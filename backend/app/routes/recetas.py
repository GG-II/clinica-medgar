"""
Rutas de Recetas
Endpoints para gestión de recetas médicas
"""
from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from io import BytesIO
from app.extensions import db
from app.models import Receta, Medicamento
from app.services.receta_service import RecetaService
from app.utils.decorators import role_required

bp = Blueprint('recetas', __name__, url_prefix='/api/recetas')


@bp.route('', methods=['GET'])
@jwt_required()
def listar_recetas():
    """
    Lista recetas con filtros opcionales
    Query params:
        - paciente_id: int
        - medico_id: int
        - activas: bool (solo recetas activas)
    """
    try:
        paciente_id = request.args.get('paciente_id', type=int)
        medico_id = request.args.get('medico_id', type=int)
        solo_activas = request.args.get('activas', 'false').lower() == 'true'
        
        query = Receta.query
        
        if paciente_id:
            query = query.filter_by(paciente_id=paciente_id)
        
        if medico_id:
            query = query.filter_by(medico_id=medico_id)
        
        if solo_activas:
            query = query.filter_by(activa=True)
        
        recetas = query.order_by(Receta.fecha_emision.desc()).all()
        
        return jsonify({
            'success': True,
            'data': [receta.to_dict(include_medicamentos=True) for receta in recetas],
            'total': len(recetas)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al listar recetas: {str(e)}'
        }), 500


@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def obtener_receta(id):
    """Obtiene una receta por ID"""
    try:
        receta = Receta.query.get(id)
        if not receta:
            return jsonify({
                'success': False,
                'message': 'Receta no encontrada'
            }), 404
        
        return jsonify({
            'success': True,
            'data': receta.to_dict(include_medicamentos=True)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener receta: {str(e)}'
        }), 500


@bp.route('', methods=['POST'])
@jwt_required()
@role_required('medico')
def crear_receta():
    """
    Crea una nueva receta
    Body: {
        "paciente_id": int,
        "medico_id": int,
        "consulta_id": int (opcional),
        "diagnostico": str (opcional),
        "indicaciones_generales": str (opcional),
        "medicamentos": [
            {
                "medicamento_id": int,
                "dosis": str,
                "frecuencia": str,
                "duracion": str (opcional),
                "via_administracion": str (opcional),
                "indicaciones_especificas": str (opcional),
                "cantidad_prescrita": int (opcional)
            }
        ]
    }
    """
    try:
        data = request.get_json()
        usuario_id = get_jwt_identity()
        
        # Validar campos requeridos
        if 'paciente_id' not in data or 'medico_id' not in data:
            return jsonify({
                'success': False,
                'message': 'paciente_id y medico_id son requeridos'
            }), 400
        
        if 'medicamentos' not in data or not data['medicamentos']:
            return jsonify({
                'success': False,
                'message': 'Debe incluir al menos un medicamento'
            }), 400
        
        # Validar cada medicamento
        for med in data['medicamentos']:
            if 'medicamento_id' not in med or 'dosis' not in med or 'frecuencia' not in med:
                return jsonify({
                    'success': False,
                    'message': 'Cada medicamento debe tener: medicamento_id, dosis y frecuencia'
                }), 400
        
        # Crear receta usando el servicio
        receta, error = RecetaService.crear_receta(data, usuario_id)
        
        if error:
            # Si hay alertas de alergias, retornar warning pero con éxito
            if '⚠️ ALERTAS' in error:
                return jsonify({
                    'success': True,
                    'warning': error,
                    'message': 'Receta creada con alertas',
                    'data': receta.to_dict(include_medicamentos=True)
                }), 201
            else:
                return jsonify({
                    'success': False,
                    'message': error
                }), 400
        
        return jsonify({
            'success': True,
            'message': 'Receta creada exitosamente',
            'data': receta.to_dict(include_medicamentos=True)
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al crear receta: {str(e)}'
        }), 500


@bp.route('/<int:id>/pdf', methods=['GET'])
@jwt_required()
def descargar_pdf(id):
    """
    Genera y descarga PDF de la receta
    """
    try:
        pdf_bytes, error = RecetaService.generar_pdf(id)
        
        if error:
            return jsonify({
                'success': False,
                'message': error
            }), 400
        
        # Crear objeto BytesIO para enviar el PDF
        pdf_file = BytesIO(pdf_bytes)
        pdf_file.seek(0)
        
        return send_file(
            pdf_file,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'receta_{id}.pdf'
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al generar PDF: {str(e)}'
        }), 500


@bp.route('/<int:id>/desactivar', methods=['PUT'])
@jwt_required()
@role_required('medico', 'administrador')
def desactivar_receta(id):
    """Desactiva una receta (ya no se puede dispensar)"""
    try:
        usuario_id = get_jwt_identity()
        
        exitoso, mensaje = RecetaService.desactivar_receta(id, usuario_id)
        
        if not exitoso:
            return jsonify({
                'success': False,
                'message': mensaje
            }), 400
        
        return jsonify({
            'success': True,
            'message': mensaje
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al desactivar receta: {str(e)}'
        }), 500


@bp.route('/paciente/<int:paciente_id>', methods=['GET'])
@jwt_required()
def historial_paciente(paciente_id):
    """
    Obtiene historial de recetas de un paciente
    Query params:
        - activas: bool (solo recetas activas)
    """
    try:
        solo_activas = request.args.get('activas', 'false').lower() == 'true'
        
        recetas = RecetaService.obtener_recetas_paciente(paciente_id, solo_activas)
        
        return jsonify({
            'success': True,
            'data': [receta.to_dict(include_medicamentos=True) for receta in recetas],
            'total': len(recetas)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener historial: {str(e)}'
        }), 500


# ========== ENDPOINTS DE MEDICAMENTOS ==========

@bp.route('/medicamentos', methods=['GET'])
@jwt_required()
def buscar_medicamentos():
    """
    Búsqueda de medicamentos
    Query params:
        - q: str (término de búsqueda)
        - limit: int (default 10)
    """
    try:
        query = request.args.get('q', '')
        limit = request.args.get('limit', 10, type=int)
        
        if not query:
            # Si no hay búsqueda, retornar los más usados
            medicamentos = Medicamento.query.filter_by(activo=True).limit(limit).all()
        else:
            medicamentos = Medicamento.buscar(query, limit)
        
        return jsonify({
            'success': True,
            'data': [med.to_dict_simple() for med in medicamentos],
            'total': len(medicamentos)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al buscar medicamentos: {str(e)}'
        }), 500


@bp.route('/medicamentos/<int:id>', methods=['GET'])
@jwt_required()
def obtener_medicamento(id):
    """Obtiene información completa de un medicamento"""
    try:
        medicamento = Medicamento.query.get(id)
        if not medicamento:
            return jsonify({
                'success': False,
                'message': 'Medicamento no encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'data': medicamento.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener medicamento: {str(e)}'
        }), 500


@bp.route('/medicamentos', methods=['POST'])
@jwt_required()
@role_required('medico', 'administrador')
def agregar_medicamento():
    """
    Agrega un medicamento personalizado al catálogo
    Body: {
        "nombre_generico": str,
        "nombre_comercial": str (opcional),
        "presentacion": str (opcional),
        "concentracion": str (opcional),
        "via_administracion": str (opcional),
        "interacciones": str (opcional),
        "contraindicaciones": str (opcional),
        "observaciones": str (opcional)
    }
    """
    try:
        data = request.get_json()
        
        if 'nombre_generico' not in data:
            return jsonify({
                'success': False,
                'message': 'nombre_generico es requerido'
            }), 400
        
        medicamento = Medicamento(
            nombre_generico=data['nombre_generico'],
            nombre_comercial=data.get('nombre_comercial'),
            presentacion=data.get('presentacion'),
            concentracion=data.get('concentracion'),
            via_administracion=data.get('via_administracion'),
            interacciones=data.get('interacciones'),
            contraindicaciones=data.get('contraindicaciones'),
            observaciones=data.get('observaciones'),
            activo=True
        )
        
        db.session.add(medicamento)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Medicamento agregado exitosamente',
            'data': medicamento.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error al agregar medicamento: {str(e)}'
        }), 500
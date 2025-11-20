"""
Rutas de Laboratorios
Endpoints para gestión de estudios de laboratorio
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Laboratorio, TipoLaboratorio, ValorReferencia
from app.services.laboratorio_service import LaboratorioService
from app.utils.decorators import role_required

bp = Blueprint('laboratorios', __name__, url_prefix='/api/laboratorios')


@bp.route('', methods=['GET'])
@jwt_required()
def listar_laboratorios():
    """
    Lista laboratorios con filtros opcionales
    Query params:
        - paciente_id: int
        - medico_id: int
        - estado: solicitado|en_proceso|completado|cancelado
        - tipo_laboratorio_id: int
    """
    try:
        paciente_id = request.args.get('paciente_id', type=int)
        medico_id = request.args.get('medico_id', type=int)
        estado = request.args.get('estado')
        tipo_laboratorio_id = request.args.get('tipo_laboratorio_id', type=int)
        
        query = Laboratorio.query
        
        if paciente_id:
            query = query.filter_by(paciente_id=paciente_id)
        
        if medico_id:
            query = query.filter_by(medico_id=medico_id)
        
        if estado:
            query = query.filter_by(estado=estado)
        
        if tipo_laboratorio_id:
            query = query.filter_by(tipo_laboratorio_id=tipo_laboratorio_id)
        
        laboratorios = query.order_by(Laboratorio.fecha_solicitud.desc()).all()
        
        return jsonify({
            'success': True,
            'data': [lab.to_dict(include_relaciones=True) for lab in laboratorios],
            'total': len(laboratorios)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al listar laboratorios: {str(e)}'
        }), 500


@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def obtener_laboratorio(id):
    """Obtiene un laboratorio por ID"""
    try:
        laboratorio = Laboratorio.query.get(id)
        if not laboratorio:
            return jsonify({
                'success': False,
                'message': 'Laboratorio no encontrado'
            }), 404
        
        # Verificar valores críticos si tiene resultados
        alertas = []
        if laboratorio.resultados and laboratorio.estado == 'completado':
            alertas = laboratorio.verificar_valores_criticos()
        
        data = laboratorio.to_dict(include_relaciones=True)
        data['alertas'] = alertas
        
        return jsonify({
            'success': True,
            'data': data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener laboratorio: {str(e)}'
        }), 500


@bp.route('', methods=['POST'])
@jwt_required()
@role_required('medico')
def solicitar_laboratorio():
    """
    Solicita un nuevo estudio de laboratorio
    Body: {
        "paciente_id": int,
        "medico_id": int,
        "tipo_laboratorio_id": int,
        "fecha_solicitud": "YYYY-MM-DD" (opcional, default hoy),
        "observaciones": str (opcional)
    }
    """
    try:
        data = request.get_json()
        usuario_id = get_jwt_identity()
        
        # Validar campos requeridos
        campos_requeridos = ['paciente_id', 'medico_id', 'tipo_laboratorio_id']
        for campo in campos_requeridos:
            if campo not in data:
                return jsonify({
                    'success': False,
                    'message': f'Campo requerido faltante: {campo}'
                }), 400
        
        # Solicitar usando el servicio
        laboratorio, error = LaboratorioService.solicitar_laboratorio(data, usuario_id)
        
        if error:
            return jsonify({
                'success': False,
                'message': error
            }), 400
        
        return jsonify({
            'success': True,
            'message': 'Laboratorio solicitado exitosamente',
            'data': laboratorio.to_dict(include_relaciones=True)
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al solicitar laboratorio: {str(e)}'
        }), 500


@bp.route('/<int:id>/resultados', methods=['PUT'])
@jwt_required()
@role_required('medico', 'enfermera')
def registrar_resultados(id):
    """
    Registra resultados de un laboratorio
    Body: {
        "fecha_resultado": "YYYY-MM-DD" (opcional, default hoy),
        "resultados": {
            "parametro1": {"valor": 12.5, "unidad": "g/dL"},
            "parametro2": {"valor": 95, "unidad": "mg/dL"}
        },
        "interpretacion": str (opcional),
        "laboratorio_externo": str (opcional),
        "archivo_url": str (opcional)
    }
    """
    try:
        data = request.get_json()
        usuario_id = get_jwt_identity()
        
        if 'resultados' not in data:
            return jsonify({
                'success': False,
                'message': 'Debe incluir los resultados'
            }), 400
        
        # Registrar usando el servicio
        laboratorio, alertas, error = LaboratorioService.registrar_resultados(
            id, data, usuario_id
        )
        
        if error:
            return jsonify({
                'success': False,
                'message': error
            }), 400
        
        response_data = {
            'success': True,
            'message': 'Resultados registrados exitosamente',
            'data': laboratorio.to_dict(include_relaciones=True)
        }
        
        # Agregar alertas si existen
        if alertas:
            response_data['alertas'] = alertas
            response_data['warning'] = f'⚠️ Se detectaron {len(alertas)} valores críticos'
        
        return jsonify(response_data), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al registrar resultados: {str(e)}'
        }), 500


@bp.route('/<int:id>/cancelar', methods=['PUT'])
@jwt_required()
@role_required('medico', 'administrador')
def cancelar_laboratorio(id):
    """
    Cancela un laboratorio solicitado
    Body: {
        "motivo": str (opcional)
    }
    """
    try:
        data = request.get_json() or {}
        usuario_id = get_jwt_identity()
        motivo = data.get('motivo')
        
        exitoso, mensaje = LaboratorioService.cancelar_laboratorio(id, usuario_id, motivo)
        
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
            'message': f'Error al cancelar laboratorio: {str(e)}'
        }), 500


@bp.route('/paciente/<int:paciente_id>', methods=['GET'])
@jwt_required()
def historial_paciente(paciente_id):
    """
    Obtiene historial de laboratorios de un paciente
    Query params:
        - completados: bool (solo completados)
    """
    try:
        solo_completados = request.args.get('completados', 'false').lower() == 'true'
        
        laboratorios = LaboratorioService.obtener_laboratorios_paciente(
            paciente_id, 
            solo_completados
        )
        
        return jsonify({
            'success': True,
            'data': [lab.to_dict(include_relaciones=True) for lab in laboratorios],
            'total': len(laboratorios)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener historial: {str(e)}'
        }), 500


@bp.route('/historico/<int:paciente_id>/<int:tipo_laboratorio_id>/<string:parametro>', methods=['GET'])
@jwt_required()
def historico_parametro(paciente_id, tipo_laboratorio_id, parametro):
    """
    Obtiene histórico de un parámetro específico para gráficas
    Query params:
        - limite: int (default 10)
    """
    try:
        limite = request.args.get('limite', 10, type=int)
        
        historico = LaboratorioService.obtener_historico_parametro(
            paciente_id,
            tipo_laboratorio_id,
            parametro,
            limite
        )
        
        return jsonify({
            'success': True,
            'data': historico,
            'total': len(historico)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener histórico: {str(e)}'
        }), 500


@bp.route('/comparar/<int:paciente_id>/<int:tipo_laboratorio_id>', methods=['GET'])
@jwt_required()
def comparar_resultados(paciente_id, tipo_laboratorio_id):
    """
    Compara últimos 3 resultados del mismo tipo de laboratorio
    """
    try:
        comparacion, error = LaboratorioService.comparar_resultados(
            paciente_id,
            tipo_laboratorio_id
        )
        
        if error:
            return jsonify({
                'success': False,
                'message': error
            }), 400
        
        return jsonify({
            'success': True,
            'data': comparacion
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al comparar resultados: {str(e)}'
        }), 500


# ========== ENDPOINTS DE TIPOS Y VALORES DE REFERENCIA ==========

@bp.route('/tipos', methods=['GET'])
@jwt_required()
def listar_tipos():
    """
    Lista todos los tipos de laboratorio disponibles
    Query params:
        - categoria: str (opcional)
    """
    try:
        categoria = request.args.get('categoria')
        
        query = TipoLaboratorio.query.filter_by(activo=True)
        
        if categoria:
            query = query.filter_by(categoria=categoria)
        
        tipos = query.order_by(TipoLaboratorio.categoria, TipoLaboratorio.nombre).all()
        
        # Agrupar por categoría
        por_categoria = {}
        for tipo in tipos:
            cat = tipo.categoria or 'Otros'
            if cat not in por_categoria:
                por_categoria[cat] = []
            por_categoria[cat].append(tipo.to_dict())
        
        return jsonify({
            'success': True,
            'data': [tipo.to_dict() for tipo in tipos],
            'por_categoria': por_categoria,
            'total': len(tipos)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al listar tipos: {str(e)}'
        }), 500


@bp.route('/tipos/<int:id>', methods=['GET'])
@jwt_required()
def obtener_tipo(id):
    """Obtiene un tipo de laboratorio con sus valores de referencia"""
    try:
        tipo = TipoLaboratorio.query.get(id)
        if not tipo:
            return jsonify({
                'success': False,
                'message': 'Tipo de laboratorio no encontrado'
            }), 404
        
        data = tipo.to_dict()
        data['valores_referencia'] = [vr.to_dict() for vr in tipo.valores_referencia]
        
        return jsonify({
            'success': True,
            'data': data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener tipo: {str(e)}'
        }), 500


@bp.route('/valores-referencia', methods=['GET'])
@jwt_required()
def obtener_valores_referencia():
    """
    Obtiene valores de referencia para un tipo de laboratorio
    Query params:
        - tipo_laboratorio_id: int (requerido)
        - parametro: str (opcional)
        - edad: int (opcional)
        - sexo: M|F (opcional)
    """
    try:
        tipo_lab_id = request.args.get('tipo_laboratorio_id', type=int)
        parametro = request.args.get('parametro')
        edad = request.args.get('edad', type=int)
        sexo = request.args.get('sexo')
        
        if not tipo_lab_id:
            return jsonify({
                'success': False,
                'message': 'tipo_laboratorio_id es requerido'
            }), 400
        
        query = ValorReferencia.query.filter_by(tipo_laboratorio_id=tipo_lab_id)
        
        if parametro:
            query = query.filter_by(parametro=parametro)
        
        # Si se proporciona edad y sexo, filtrar adecuadamente
        if edad is not None:
            query = query.filter(
                db.or_(
                    ValorReferencia.rango_edad_min.is_(None),
                    ValorReferencia.rango_edad_min <= edad
                ),
                db.or_(
                    ValorReferencia.rango_edad_max.is_(None),
                    ValorReferencia.rango_edad_max >= edad
                )
            )
        
        if sexo:
            query = query.filter(
                db.or_(
                    ValorReferencia.sexo == 'ambos',
                    ValorReferencia.sexo == sexo
                )
            )
        
        valores = query.all()
        
        return jsonify({
            'success': True,
            'data': [val.to_dict() for val in valores],
            'total': len(valores)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener valores de referencia: {str(e)}'
        }), 500


@bp.route('/categorias', methods=['GET'])
@jwt_required()
def listar_categorias():
    """Lista todas las categorías de laboratorio disponibles"""
    try:
        # Obtener categorías únicas
        categorias = db.session.query(TipoLaboratorio.categoria)\
            .filter(TipoLaboratorio.activo == True)\
            .filter(TipoLaboratorio.categoria.isnot(None))\
            .distinct()\
            .order_by(TipoLaboratorio.categoria)\
            .all()
        
        categorias_lista = [cat[0] for cat in categorias if cat[0]]
        
        return jsonify({
            'success': True,
            'data': categorias_lista,
            'total': len(categorias_lista)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al listar categorías: {str(e)}'
        }), 500
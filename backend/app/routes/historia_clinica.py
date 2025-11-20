"""
Rutas de Historia Clínica
Endpoints para gestión de historia clínica, signos vitales y antecedentes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.paciente import Paciente
from app.models.historia_clinica import HistoriaClinica
from app.models.signos_vitales import SignosVitales
from app.models.antecedentes import Antecedente
from app.models.vacuna import Vacuna, AplicacionVacuna
from app.models.auditoria import LogAuditoria
from app.utils.helpers import calcular_imc
from datetime import datetime

# Crear blueprint
historia_bp = Blueprint('historia_clinica', __name__, url_prefix='/api/historia-clinica')


@historia_bp.route('/paciente/<int:paciente_id>', methods=['GET'])
@jwt_required()
def obtener_historia_clinica(paciente_id):
    """
    Obtiene la historia clínica completa de un paciente
    
    Incluye:
    - Datos básicos de historia clínica
    - Signos vitales históricos
    - Antecedentes
    - Vacunas aplicadas
    """
    try:
        paciente = Paciente.query.get(paciente_id)
        if not paciente:
            return jsonify({
                'success': False,
                'message': 'Paciente no encontrado'
            }), 404
        
        # Obtener o crear historia clínica
        historia = HistoriaClinica.query.filter_by(paciente_id=paciente_id).first()
        if not historia:
            historia = HistoriaClinica(paciente_id=paciente_id)
            db.session.add(historia)
            db.session.commit()
        
        # Obtener datos relacionados
        signos_vitales = SignosVitales.query.filter_by(paciente_id=paciente_id)\
            .order_by(SignosVitales.fecha_registro.desc())\
            .limit(10).all()
        
        antecedentes = Antecedente.query.filter_by(paciente_id=paciente_id, activo=True)\
            .order_by(Antecedente.tipo, Antecedente.created_at.desc()).all()
        
        vacunas_aplicadas = AplicacionVacuna.query.filter_by(paciente_id=paciente_id)\
            .order_by(AplicacionVacuna.fecha_aplicacion.desc()).all()
        
        return jsonify({
            'success': True,
            'data': {
                'paciente': paciente.to_dict(),
                'historia_clinica': historia.to_dict(),
                'signos_vitales': [sv.to_dict() for sv in signos_vitales],
                'antecedentes': [ant.to_dict() for ant in antecedentes],
                'vacunas_aplicadas': [vac.to_dict() for vac in vacunas_aplicadas]
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener historia clínica: {str(e)}'
        }), 500


@historia_bp.route('/paciente/<int:paciente_id>', methods=['PUT'])
@jwt_required()
def actualizar_historia_clinica(paciente_id):
    """
    Actualiza datos generales de la historia clínica
    """
    try:
        data = request.get_json()
        
        historia = HistoriaClinica.query.filter_by(paciente_id=paciente_id).first()
        if not historia:
            historia = HistoriaClinica(paciente_id=paciente_id)
            db.session.add(historia)
        
        # Actualizar tipo de sangre
        if 'tipo_sangre' in data:
            historia.tipo_sangre = data['tipo_sangre']
        
        historia.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Historia clínica actualizada',
            'data': historia.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error al actualizar historia clínica: {str(e)}'
        }), 500


@historia_bp.route('/signos-vitales', methods=['POST'])
@jwt_required()
def registrar_signos_vitales():
    """
    Registra signos vitales de un paciente
    
    Body:
        - paciente_id: int (requerido)
        - motivo_consulta: string (opcional, para crear consulta automática)
        - presion_sistolica: int
        - presion_diastolica: int
        - frecuencia_cardiaca: int
        - temperatura: float
        - saturacion_oxigeno: int
        - frecuencia_respiratoria: int
        - peso: float
        - talla: float
        - perimetro_cefalico: float
        - frecuencia_cardiaca_fetal: int
        - observaciones: string
    """
    try:
        from app.models.consulta import Consulta
        
        data = request.get_json()
        
        if not data.get('paciente_id'):
            return jsonify({
                'success': False,
                'message': 'El paciente_id es requerido'
            }), 400
        
        usuario_id = int(get_jwt_identity())
        
        # Crear consulta automáticamente si no viene consulta_id
        consulta_id = data.get('consulta_id')
        if not consulta_id:
            motivo = data.get('motivo_consulta', 'Consulta general')
            consulta = Consulta(
                paciente_id=data['paciente_id'],
                medico_id=usuario_id,
                motivo_consulta=motivo,
                fecha_consulta=datetime.utcnow()
            )
            db.session.add(consulta)
            db.session.flush()  # Para obtener el ID
            consulta_id = consulta.id
        
        # Calcular IMC si hay peso y talla
        imc = None
        if data.get('peso') and data.get('talla'):
            imc = calcular_imc(data['peso'], data['talla'])
        
        signos = SignosVitales(
            paciente_id=data['paciente_id'],
            consulta_id=consulta_id,
            presion_sistolica=data.get('presion_sistolica'),
            presion_diastolica=data.get('presion_diastolica'),
            frecuencia_cardiaca=data.get('frecuencia_cardiaca'),
            temperatura=data.get('temperatura'),
            saturacion_oxigeno=data.get('saturacion_oxigeno'),
            frecuencia_respiratoria=data.get('frecuencia_respiratoria'),
            peso=data.get('peso'),
            talla=data.get('talla'),
            imc=imc,
            perimetro_cefalico=data.get('perimetro_cefalico'),
            frecuencia_cardiaca_fetal=data.get('frecuencia_cardiaca_fetal'),
            observaciones=data.get('observaciones')
        )
        
        db.session.add(signos)
        db.session.commit()
        
        LogAuditoria.registrar(
            usuario_id=usuario_id,
            accion='registrar_signos_vitales',
            tabla_afectada='signos_vitales',
            registro_id=signos.id,
            detalles=f"Signos vitales registrados para paciente {data['paciente_id']}"
        )
        
        return jsonify({
            'success': True,
            'message': 'Signos vitales registrados',
            'data': signos.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error al registrar signos vitales: {str(e)}'
        }), 500


@historia_bp.route('/antecedentes', methods=['POST'])
@jwt_required()
def registrar_antecedente():
    """
    Registra un antecedente del paciente
    
    Body:
        - paciente_id: int (requerido)
        - tipo: string (requerido) - medicos, quirurgicos, traumaticos, alergicos, ginecologicos, obstetricos
        - descripcion: string (requerido)
        - fecha_evento: date (opcional)
        - relevancia: string (opcional) - alta, media, baja
    """
    try:
        data = request.get_json()
        
        if not data.get('paciente_id') or not data.get('tipo') or not data.get('descripcion'):
            return jsonify({
                'success': False,
                'message': 'paciente_id, tipo y descripcion son requeridos'
            }), 400
        
        antecedente = Antecedente(
            paciente_id=data['paciente_id'],
            tipo=data['tipo'],
            descripcion=data['descripcion'],
            fecha_evento=datetime.strptime(data['fecha_evento'], '%Y-%m-%d').date() if data.get('fecha_evento') else None,
            relevancia=data.get('relevancia', 'media')
        )
        
        db.session.add(antecedente)
        db.session.commit()
        
        usuario_id = get_jwt_identity()
        LogAuditoria.registrar(
            usuario_id=int(usuario_id),
            accion='registrar_antecedente',
            tabla_afectada='antecedentes',
            registro_id=antecedente.id,
            detalles=f"Antecedente {data['tipo']} registrado para paciente {data['paciente_id']}"
        )
        
        return jsonify({
            'success': True,
            'message': 'Antecedente registrado',
            'data': antecedente.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error al registrar antecedente: {str(e)}'
        }), 500


@historia_bp.route('/antecedentes/<int:antecedente_id>', methods=['DELETE'])
@jwt_required()
def eliminar_antecedente(antecedente_id):
    """
    Elimina (desactiva) un antecedente
    """
    try:
        antecedente = Antecedente.query.get(antecedente_id)
        
        if not antecedente:
            return jsonify({
                'success': False,
                'message': 'Antecedente no encontrado'
            }), 404
        
        antecedente.activo = False
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Antecedente eliminado'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error al eliminar antecedente: {str(e)}'
        }), 500


@historia_bp.route('/vacunas', methods=['GET'])
@jwt_required()
def obtener_catalogo_vacunas():
    """
    Obtiene el catálogo de vacunas disponibles
    """
    try:
        vacunas = Vacuna.query.filter_by(activo=True).order_by(Vacuna.nombre).all()
        
        return jsonify({
            'success': True,
            'data': [v.to_dict() for v in vacunas]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener catálogo de vacunas: {str(e)}'
        }), 500


@historia_bp.route('/vacunas/aplicar', methods=['POST'])
@jwt_required()
def aplicar_vacuna():
    """
    Registra la aplicación de una vacuna a un paciente
    
    Body:
        - paciente_id: int (requerido)
        - vacuna_id: int (requerido)
        - numero_dosis: int (requerido)
        - fecha_aplicacion: date (requerido)
        - lote: string (opcional)
        - aplicada_por: string (opcional)
        - observaciones: string (opcional)
    """
    try:
        data = request.get_json()
        
        if not all(k in data for k in ['paciente_id', 'vacuna_id', 'numero_dosis', 'fecha_aplicacion']):
            return jsonify({
                'success': False,
                'message': 'Faltan campos requeridos'
            }), 400
        
        aplicacion = AplicacionVacuna(
            paciente_id=data['paciente_id'],
            vacuna_id=data['vacuna_id'],
            numero_dosis=data['numero_dosis'],
            fecha_aplicacion=datetime.strptime(data['fecha_aplicacion'], '%Y-%m-%d').date(),
            lote=data.get('lote'),
            aplicada_por=data.get('aplicada_por'),
            observaciones=data.get('observaciones')
        )
        
        db.session.add(aplicacion)
        db.session.commit()
        
        usuario_id = get_jwt_identity()
        LogAuditoria.registrar(
            usuario_id=int(usuario_id),
            accion='aplicar_vacuna',
            tabla_afectada='aplicaciones_vacunas',
            registro_id=aplicacion.id,
            detalles=f"Vacuna aplicada a paciente {data['paciente_id']}"
        )
        
        return jsonify({
            'success': True,
            'message': 'Vacuna aplicada exitosamente',
            'data': aplicacion.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error al aplicar vacuna: {str(e)}'
        }), 500
"""
Rutas de Uploads
Endpoints para subir y gestionar archivos de pacientes
"""
from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.archivo_service import ArchivoService
import os

# Crear blueprint
uploads_bp = Blueprint('uploads', __name__, url_prefix='/api/uploads')


@uploads_bp.route('/paciente/<int:paciente_id>', methods=['POST'])
@jwt_required()
def subir_archivo(paciente_id):
    """
    Sube un archivo para un paciente
    
    Form Data:
        - file: archivo (requerido)
        - categoria: string (requerido) - laboratorios, imagenes, recetas, ekg, otros
        - descripcion: string (opcional)
    """
    try:
        # Validar que hay archivo
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'message': 'No se proporcionó archivo'
            }), 400
        
        file = request.files['file']
        categoria = request.form.get('categoria')
        descripcion = request.form.get('descripcion')
        
        if not categoria:
            return jsonify({
                'success': False,
                'message': 'La categoría es requerida'
            }), 400
        
        usuario_id = int(get_jwt_identity())
        
        # Guardar archivo
        archivo, error = ArchivoService.guardar_archivo(
            file=file,
            paciente_id=paciente_id,
            categoria=categoria,
            descripcion=descripcion,
            usuario_id=usuario_id
        )
        
        if error:
            return jsonify({
                'success': False,
                'message': error
            }), 400
        
        return jsonify({
            'success': True,
            'message': 'Archivo subido exitosamente',
            'data': archivo.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al subir archivo: {str(e)}'
        }), 500


@uploads_bp.route('/paciente/<int:paciente_id>', methods=['GET'])
@jwt_required()
def listar_archivos(paciente_id):
    """
    Lista los archivos de un paciente
    
    Query params:
        - categoria: string (opcional) - filtrar por categoría
    """
    try:
        categoria = request.args.get('categoria')
        
        archivos = ArchivoService.obtener_archivos_paciente(
            paciente_id=paciente_id,
            categoria=categoria
        )
        
        return jsonify({
            'success': True,
            'data': archivos
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al listar archivos: {str(e)}'
        }), 500


@uploads_bp.route('/<int:archivo_id>', methods=['DELETE'])
@jwt_required()
def eliminar_archivo(archivo_id):
    """
    Elimina un archivo
    """
    try:
        usuario_id = int(get_jwt_identity())
        
        success, error = ArchivoService.eliminar_archivo(
            archivo_id=archivo_id,
            usuario_id=usuario_id
        )
        
        if error:
            return jsonify({
                'success': False,
                'message': error
            }), 404 if 'no encontrado' in error else 500
        
        return jsonify({
            'success': True,
            'message': 'Archivo eliminado exitosamente'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al eliminar archivo: {str(e)}'
        }), 500


@uploads_bp.route('/download/<int:archivo_id>', methods=['GET'])
@jwt_required()
def descargar_archivo(archivo_id):
    """
    Descarga un archivo
    """
    try:
        from app.models.archivo_paciente import ArchivoPaciente
        
        archivo = ArchivoPaciente.query.get(archivo_id)
        
        if not archivo:
            return jsonify({
                'success': False,
                'message': 'Archivo no encontrado'
            }), 404
        
        if not os.path.exists(archivo.ruta_archivo):
            return jsonify({
                'success': False,
                'message': 'Archivo físico no encontrado'
            }), 404
        
        return send_file(
            archivo.ruta_archivo,
            as_attachment=True,
            download_name=archivo.nombre_archivo
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al descargar archivo: {str(e)}'
        }), 500
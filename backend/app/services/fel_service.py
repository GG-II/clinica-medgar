"""
Servicio para integración con FEL (Factura Electrónica en Línea) Guatemala.
NOTA: Estructura base - Integración completa en Fase 7
"""

from app.models import Factura, FacturaDetalle
from datetime import datetime

class FELService:
    """
    Servicio para integración con certificadores FEL de Guatemala.
    Proveedores certificados: INFILE, DIGIFACT, G4S, etc.
    """
    
    @staticmethod
    def preparar_datos_fel(factura_id):
        """
        Prepara los datos de la factura en el formato requerido por SAT Guatemala.
        
        Estructura según régimen FEL:
        - Emisor (datos de la clínica)
        - Receptor (datos del cliente/paciente)
        - Items (productos/servicios)
        - Totales
        - Información tributaria
        """
        factura = Factura.query.get(factura_id)
        
        if not factura:
            raise ValueError('Factura no encontrada')
        
        # TODO Fase 7: Obtener datos de la clínica desde configuración
        datos_emisor = {
            'nit': '1234567-8',  # TODO: Configurar NIT real
            'nombre': 'Clínica Médica Dra. Estephanny García',
            'nombre_comercial': 'Clínica Dra. García',
            'direccion': {
                'direccion': 'Dirección de la clínica',  # TODO: Configurar
                'codigo_postal': '01001',
                'municipio': 'Guatemala',
                'departamento': 'Guatemala',
                'pais': 'GT'
            },
            'correo_electronico': 'facturacion@clinica.com',  # TODO: Configurar
            'afiliacion_iva': 'GEN'  # Régimen General
        }
        
        # Datos del receptor (paciente/cliente)
        datos_receptor = {
            'nit': factura.nit_cliente or 'CF',  # CF = Consumidor Final
            'nombre': factura.nombre_cliente or factura.paciente.nombre_completo,
            'direccion': {
                'direccion': factura.direccion_cliente or factura.paciente.direccion or 'Ciudad',
                'codigo_postal': '01001',
                'municipio': 'Guatemala',
                'departamento': 'Guatemala',
                'pais': 'GT'
            }
        }
        
        # Items de la factura
        items = []
        for detalle in factura.detalles:
            items.append({
                'bien_o_servicio': 'S',  # S = Servicio, B = Bien
                'numero_linea': len(items) + 1,
                'cantidad': detalle.cantidad,
                'unidad_medida': 'UNI',  # Unidad
                'descripcion': detalle.descripcion,
                'precio_unitario': float(detalle.precio_unitario),
                'precio': float(detalle.subtotal),
                'descuento': 0,
                'total': float(detalle.subtotal)
            })
        
        # Totales
        totales = {
            'gran_total': float(factura.total),
            'total_impuestos': float(factura.impuestos or 0)
        }
        
        # Estructura completa FEL
        datos_fel = {
            'emisor': datos_emisor,
            'receptor': datos_receptor,
            'frases': [
                {
                    'tipo_frase': 1,  # Sujeto a pagos trimestrales
                    'codigo_escenario': 1
                }
            ],
            'items': items,
            'totales': totales,
            'complementos': []
        }
        
        return datos_fel
    
    @staticmethod
    def certificar_factura(factura_id):
        """
        Certifica la factura con el proveedor FEL.
        
        NOTA: Implementación completa en Fase 7
        - Conectar con API del certificador
        - Enviar XML firmado
        - Recibir UUID de SAT
        - Almacenar XML certificado
        """
        datos_fel = FELService.preparar_datos_fel(factura_id)
        
        # TODO Fase 7: Implementar conexión con API del certificador
        # Ejemplo con INFILE o DIGIFACT:
        # response = requests.post(
        #     url='https://api.certificador.com/certificar',
        #     headers={'Authorization': 'Bearer TOKEN'},
        #     json=datos_fel
        # )
        
        # Por ahora, retornamos estructura de respuesta simulada
        return {
            'success': False,
            'message': 'Certificación FEL pendiente de implementación (Fase 7)',
            'datos_preparados': datos_fel,
            'uuid': None,
            'xml': None
        }
    
    @staticmethod
    def anular_factura_fel(factura_id, motivo):
        """
        Anula una factura certificada con FEL.
        
        NOTA: Implementación completa en Fase 7
        """
        factura = Factura.query.get(factura_id)
        
        if not factura:
            raise ValueError('Factura no encontrada')
        
        if not factura.certificada_fel:
            raise ValueError('La factura no está certificada con FEL')
        
        # TODO Fase 7: Implementar anulación con API del certificador
        
        return {
            'success': False,
            'message': 'Anulación FEL pendiente de implementación (Fase 7)',
            'motivo': motivo
        }
    
    @staticmethod
    def validar_nit(nit):
        """
        Valida un NIT de Guatemala.
        Algoritmo de validación según SAT Guatemala.
        """
        if not nit or nit == 'CF':
            return True  # CF (Consumidor Final) es válido
        
        # Remover guiones y espacios
        nit_limpio = nit.replace('-', '').replace(' ', '')
        
        # Debe tener entre 8 y 9 dígitos
        if not nit_limpio.isdigit() or len(nit_limpio) not in [8, 9]:
            return False
        
        # Algoritmo de validación NIT Guatemala
        if len(nit_limpio) == 8:
            # NIT de 8 dígitos (antiguo)
            factor = len(nit_limpio) + 1
            suma = 0
            
            for digito in nit_limpio:
                suma += int(digito) * factor
                factor -= 1
            
            modulo = suma % 11
            digito_verificador = 0 if modulo == 0 else 11 - modulo
            
            # El último dígito debe ser el verificador
            return int(nit_limpio[-1]) == digito_verificador
        
        else:
            # NIT de 9 dígitos (nuevo formato)
            # Validación simplificada - en producción usar servicio de SAT
            return True
    
    @staticmethod
    def obtener_regimen_fel():
        """
        Retorna el régimen FEL de la clínica.
        Opciones: PEQ (Pequeño Contribuyente), GEN (Régimen General)
        
        TODO Fase 7: Obtener desde configuración
        """
        return 'GEN'  # Régimen General por defecto
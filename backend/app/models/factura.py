"""
Modelos para Facturación y Cuentas por Cobrar.
Incluye: Convenio, Factura, FacturaDetalle, CuentaPorCobrar, PagoCuenta
"""

from app.extensions import db
from datetime import datetime

class Convenio(db.Model):
    """
    Modelo para convenios con IGSS y aseguradoras.
    """
    __tablename__ = 'convenios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(
        db.Enum('igss', 'seguro_privado', 'empresa', name='tipo_convenio'),
        nullable=False
    )
    nit = db.Column(db.String(20))
    contacto_nombre = db.Column(db.String(100))
    contacto_telefono = db.Column(db.String(20))
    contacto_email = db.Column(db.String(100))
    porcentaje_cobertura = db.Column(db.Numeric(5, 2))  # 0-100%
    dias_credito = db.Column(db.Integer, default=30)
    activo = db.Column(db.Boolean, default=True)
    observaciones = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    facturas = db.relationship('Factura', back_populates='convenio', lazy='dynamic')
    cuentas_por_cobrar = db.relationship('CuentaPorCobrar', back_populates='convenio', lazy='dynamic')
    
    def __repr__(self):
        return f'<Convenio {self.id} - {self.nombre}>'
    
    def to_dict(self):
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'tipo': self.tipo,
            'nit': self.nit,
            'contacto_nombre': self.contacto_nombre,
            'contacto_telefono': self.contacto_telefono,
            'contacto_email': self.contacto_email,
            'porcentaje_cobertura': float(self.porcentaje_cobertura) if self.porcentaje_cobertura else None,
            'dias_credito': self.dias_credito,
            'activo': self.activo,
            'observaciones': self.observaciones,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Factura(db.Model):
    """
    Modelo para facturas con preparación FEL Guatemala.
    """
    __tablename__ = 'facturas'
    
    id = db.Column(db.Integer, primary_key=True)
    numero_factura = db.Column(db.String(50), unique=True, nullable=False)
    serie = db.Column(db.String(10))
    uuid_fel = db.Column(db.String(100), unique=True)  # UUID de SAT Guatemala
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    convenio_id = db.Column(db.Integer, db.ForeignKey('convenios.id'))
    fecha_emision = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    nit_cliente = db.Column(db.String(20))
    nombre_cliente = db.Column(db.String(150))
    direccion_cliente = db.Column(db.Text)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    descuento = db.Column(db.Numeric(10, 2), default=0)
    impuestos = db.Column(db.Numeric(10, 2), default=0)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    forma_pago = db.Column(
        db.Enum('efectivo', 'transferencia', 'tarjeta', 'credito', name='forma_pago_factura'),
        default='efectivo'
    )
    estado = db.Column(
        db.Enum('pendiente', 'pagada', 'anulada', 'credito', name='estado_factura'),
        default='pendiente',
        nullable=False
    )
    certificada_fel = db.Column(db.Boolean, default=False)
    xml_fel = db.Column(db.Text)  # XML firmado de FEL
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    observaciones = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    paciente = db.relationship('Paciente')
    convenio = db.relationship('Convenio', back_populates='facturas')
    usuario = db.relationship('Usuario')
    detalles = db.relationship('FacturaDetalle', back_populates='factura', lazy='dynamic', cascade='all, delete-orphan')
    cuenta_por_cobrar = db.relationship('CuentaPorCobrar', back_populates='factura', uselist=False)
    
    def __repr__(self):
        return f'<Factura {self.numero_factura} - Q{self.total}>'
    
    def to_dict(self, incluir_relaciones=False):
        """Convierte el modelo a diccionario"""
        data = {
            'id': self.id,
            'numero_factura': self.numero_factura,
            'serie': self.serie,
            'uuid_fel': self.uuid_fel,
            'paciente_id': self.paciente_id,
            'convenio_id': self.convenio_id,
            'fecha_emision': self.fecha_emision.isoformat() if self.fecha_emision else None,
            'nit_cliente': self.nit_cliente,
            'nombre_cliente': self.nombre_cliente,
            'direccion_cliente': self.direccion_cliente,
            'subtotal': float(self.subtotal),
            'descuento': float(self.descuento),
            'impuestos': float(self.impuestos),
            'total': float(self.total),
            'forma_pago': self.forma_pago,
            'estado': self.estado,
            'certificada_fel': self.certificada_fel,
            'usuario_id': self.usuario_id,
            'observaciones': self.observaciones,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if incluir_relaciones:
            data['paciente'] = {
                'id': self.paciente.id,
                'nombre_completo': self.paciente.nombre_completo
            } if self.paciente else None
            
            data['convenio'] = self.convenio.to_dict() if self.convenio else None
            data['detalles'] = [detalle.to_dict() for detalle in self.detalles]
        
        return data
    
    def calcular_totales(self):
        """Calcula subtotal, impuestos y total"""
        self.subtotal = sum(detalle.subtotal for detalle in self.detalles)
        subtotal_con_descuento = self.subtotal - self.descuento
        self.impuestos = subtotal_con_descuento * 0.12  # IVA 12% Guatemala
        self.total = subtotal_con_descuento + self.impuestos
    
    def anular(self, motivo=None):
        """Anula la factura"""
        self.estado = 'anulada'
        if motivo:
            self.observaciones = f"Anulada: {motivo}"
    
    def generar_numero_factura(self, serie='A'):
        """Genera número de factura consecutivo"""
        if self.numero_factura:
            return self.numero_factura
        
        # Buscar última factura de la serie
        ultima = Factura.query.filter_by(serie=serie).order_by(Factura.id.desc()).first()
        
        if ultima and ultima.numero_factura:
            try:
                numero = int(ultima.numero_factura.split('-')[1]) + 1
            except:
                numero = 1
        else:
            numero = 1
        
        self.serie = serie
        self.numero_factura = f'{serie}-{numero:08d}'
        return self.numero_factura


class FacturaDetalle(db.Model):
    """
    Modelo para detalle de facturas (servicios/productos facturados).
    """
    __tablename__ = 'facturas_detalle'
    
    id = db.Column(db.Integer, primary_key=True)
    factura_id = db.Column(db.Integer, db.ForeignKey('facturas.id', ondelete='CASCADE'), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    tipo_servicio = db.Column(db.String(50))  # 'consulta', 'medicamento', 'laboratorio', etc.
    referencia_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    factura = db.relationship('Factura', back_populates='detalles')
    
    def __repr__(self):
        return f'<FacturaDetalle {self.id} - {self.descripcion}>'
    
    def to_dict(self):
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'factura_id': self.factura_id,
            'descripcion': self.descripcion,
            'cantidad': self.cantidad,
            'precio_unitario': float(self.precio_unitario),
            'subtotal': float(self.subtotal),
            'tipo_servicio': self.tipo_servicio,
            'referencia_id': self.referencia_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def calcular_subtotal(self):
        """Calcula el subtotal del detalle"""
        self.subtotal = self.cantidad * self.precio_unitario
        return self.subtotal


class CuentaPorCobrar(db.Model):
    """
    Modelo para cuentas por cobrar (créditos a pacientes o convenios).
    """
    __tablename__ = 'cuentas_por_cobrar'
    
    id = db.Column(db.Integer, primary_key=True)
    factura_id = db.Column(db.Integer, db.ForeignKey('facturas.id'), nullable=False)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'))
    convenio_id = db.Column(db.Integer, db.ForeignKey('convenios.id'))
    monto_total = db.Column(db.Numeric(10, 2), nullable=False)
    monto_pagado = db.Column(db.Numeric(10, 2), default=0)
    saldo_pendiente = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_vencimiento = db.Column(db.Date)
    estado = db.Column(
        db.Enum('pendiente', 'parcial', 'pagada', 'vencida', name='estado_cuenta'),
        default='pendiente',
        nullable=False
    )
    observaciones = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    factura = db.relationship('Factura', back_populates='cuenta_por_cobrar')
    paciente = db.relationship('Paciente')
    convenio = db.relationship('Convenio', back_populates='cuentas_por_cobrar')
    pagos = db.relationship('PagoCuenta', back_populates='cuenta', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<CuentaPorCobrar {self.id} - Saldo Q{self.saldo_pendiente}>'
    
    def to_dict(self, incluir_pagos=False):
        """Convierte el modelo a diccionario"""
        data = {
            'id': self.id,
            'factura_id': self.factura_id,
            'paciente_id': self.paciente_id,
            'convenio_id': self.convenio_id,
            'monto_total': float(self.monto_total),
            'monto_pagado': float(self.monto_pagado),
            'saldo_pendiente': float(self.saldo_pendiente),
            'fecha_vencimiento': self.fecha_vencimiento.isoformat() if self.fecha_vencimiento else None,
            'estado': self.estado,
            'observaciones': self.observaciones,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if incluir_pagos:
            data['pagos'] = [pago.to_dict() for pago in self.pagos]
        
        return data
    
    def registrar_pago(self, monto, forma_pago='efectivo', numero_recibo=None, 
                      usuario_id=None, observaciones=None):
        """Registra un pago y actualiza saldos"""
        if monto > self.saldo_pendiente:
            raise ValueError('El monto del pago no puede ser mayor al saldo pendiente')
        
        self.monto_pagado += monto
        self.saldo_pendiente -= monto
        self.updated_at = datetime.utcnow()
        
        # Actualizar estado
        if self.saldo_pendiente == 0:
            self.estado = 'pagada'
        elif self.monto_pagado > 0:
            self.estado = 'parcial'
        
        # Crear registro de pago
        pago = PagoCuenta(
            cuenta_id=self.id,
            monto_pago=monto,
            forma_pago=forma_pago,
            fecha_pago=datetime.utcnow(),
            numero_recibo=numero_recibo,
            usuario_id=usuario_id,
            observaciones=observaciones
        )
        
        return pago
    
    def esta_vencida(self):
        """Verifica si la cuenta está vencida"""
        if not self.fecha_vencimiento:
            return False
        return self.fecha_vencimiento < datetime.now().date() and self.saldo_pendiente > 0


class PagoCuenta(db.Model):
    """
    Modelo para pagos aplicados a cuentas por cobrar.
    """
    __tablename__ = 'pagos_cuentas'
    
    id = db.Column(db.Integer, primary_key=True)
    cuenta_id = db.Column(db.Integer, db.ForeignKey('cuentas_por_cobrar.id'), nullable=False)
    monto_pago = db.Column(db.Numeric(10, 2), nullable=False)
    forma_pago = db.Column(
        db.Enum('efectivo', 'transferencia', 'tarjeta', 'cheque', name='forma_pago_cuenta'),
        default='efectivo'
    )
    fecha_pago = db.Column(db.DateTime, nullable=False)
    numero_recibo = db.Column(db.String(50))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    observaciones = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    cuenta = db.relationship('CuentaPorCobrar', back_populates='pagos')
    usuario = db.relationship('Usuario')
    
    def __repr__(self):
        return f'<PagoCuenta {self.id} - Q{self.monto_pago}>'
    
    def to_dict(self):
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'cuenta_id': self.cuenta_id,
            'monto_pago': float(self.monto_pago),
            'forma_pago': self.forma_pago,
            'fecha_pago': self.fecha_pago.isoformat() if self.fecha_pago else None,
            'numero_recibo': self.numero_recibo,
            'usuario_id': self.usuario_id,
            'observaciones': self.observaciones,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
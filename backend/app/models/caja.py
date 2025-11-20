"""
Modelos para Caja y Control de Efectivo.
Incluye: Caja y MovimientoCaja
"""

from app.extensions import db
from datetime import datetime

class Caja(db.Model):
    """
    Modelo para apertura y cierre de caja diaria.
    Estados: abierta, cerrada
    """
    __tablename__ = 'cajas'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha_apertura = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_cierre = db.Column(db.DateTime)
    monto_inicial = db.Column(db.Numeric(10, 2), nullable=False)
    monto_final = db.Column(db.Numeric(10, 2))
    total_ingresos = db.Column(db.Numeric(10, 2))
    total_egresos = db.Column(db.Numeric(10, 2))
    efectivo_contado = db.Column(db.Numeric(10, 2))  # Conteo físico
    diferencia = db.Column(db.Numeric(10, 2))  # efectivo_contado - (monto_inicial + ingresos - egresos)
    estado = db.Column(
        db.Enum('abierta', 'cerrada', name='estado_caja'),
        default='abierta',
        nullable=False
    )
    observaciones = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    usuario = db.relationship('Usuario')
    movimientos = db.relationship('MovimientoCaja', back_populates='caja', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Caja {self.id} - Usuario {self.usuario_id} - {self.estado}>'
    
    def to_dict(self, incluir_movimientos=False):
        """Convierte el modelo a diccionario"""
        data = {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'fecha_apertura': self.fecha_apertura.isoformat() if self.fecha_apertura else None,
            'fecha_cierre': self.fecha_cierre.isoformat() if self.fecha_cierre else None,
            'monto_inicial': float(self.monto_inicial) if self.monto_inicial else None,
            'monto_final': float(self.monto_final) if self.monto_final else None,
            'total_ingresos': float(self.total_ingresos) if self.total_ingresos else None,
            'total_egresos': float(self.total_egresos) if self.total_egresos else None,
            'efectivo_contado': float(self.efectivo_contado) if self.efectivo_contado else None,
            'diferencia': float(self.diferencia) if self.diferencia else None,
            'estado': self.estado,
            'observaciones': self.observaciones,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if incluir_movimientos:
            data['usuario'] = {
                'id': self.usuario.id,
                'nombre_completo': self.usuario.nombre_completo
            } if self.usuario else None
            data['movimientos'] = [mov.to_dict() for mov in self.movimientos]
            data['cantidad_movimientos'] = self.movimientos.count()
        
        return data
    
    def calcular_totales(self):
        """Calcula totales de ingresos y egresos"""
        self.total_ingresos = sum(
            mov.monto for mov in self.movimientos.filter_by(tipo='ingreso')
        ) or 0
        
        self.total_egresos = sum(
            mov.monto for mov in self.movimientos.filter_by(tipo='egreso')
        ) or 0
    
    def calcular_monto_esperado(self):
        """Calcula el monto esperado en caja"""
        return self.monto_inicial + (self.total_ingresos or 0) - (self.total_egresos or 0)
    
    def cerrar_caja(self, efectivo_contado, observaciones=None):
        """
        Cierra la caja y calcula diferencias.
        """
        self.calcular_totales()
        self.efectivo_contado = efectivo_contado
        
        monto_esperado = self.calcular_monto_esperado()
        self.monto_final = efectivo_contado
        self.diferencia = efectivo_contado - monto_esperado
        
        self.estado = 'cerrada'
        self.fecha_cierre = datetime.utcnow()
        
        if observaciones:
            self.observaciones = observaciones
    
    def esta_abierta(self):
        """Verifica si la caja está abierta"""
        return self.estado == 'abierta'


class MovimientoCaja(db.Model):
    """
    Modelo para movimientos de caja (ingresos y egresos).
    """
    __tablename__ = 'movimientos_caja'
    
    id = db.Column(db.Integer, primary_key=True)
    caja_id = db.Column(db.Integer, db.ForeignKey('cajas.id'), nullable=False)
    tipo = db.Column(
        db.Enum('ingreso', 'egreso', name='tipo_movimiento_caja'),
        nullable=False
    )
    categoria = db.Column(db.String(100), nullable=False)
    concepto = db.Column(db.Text, nullable=False)
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    forma_pago = db.Column(
        db.Enum('efectivo', 'transferencia', 'tarjeta', 'cheque', name='forma_pago'),
        default='efectivo'
    )
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'))
    medico_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    referencia_id = db.Column(db.Integer)  # ID de factura, compra, etc.
    referencia_tipo = db.Column(db.String(50))  # 'factura', 'compra', etc.
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    fecha_movimiento = db.Column(db.DateTime, default=datetime.utcnow)
    observaciones = db.Column(db.Text)
    
    # Relaciones
    caja = db.relationship('Caja', back_populates='movimientos')
    paciente = db.relationship('Paciente', foreign_keys=[paciente_id])
    medico = db.relationship('Usuario', foreign_keys=[medico_id])
    usuario = db.relationship('Usuario', foreign_keys=[usuario_id])
    
    def __repr__(self):
        return f'<MovimientoCaja {self.id} - {self.tipo} - Q{self.monto}>'
    
    def to_dict(self, incluir_relaciones=False):
        """Convierte el modelo a diccionario"""
        data = {
            'id': self.id,
            'caja_id': self.caja_id,
            'tipo': self.tipo,
            'categoria': self.categoria,
            'concepto': self.concepto,
            'monto': float(self.monto),
            'forma_pago': self.forma_pago,
            'paciente_id': self.paciente_id,
            'medico_id': self.medico_id,
            'referencia_id': self.referencia_id,
            'referencia_tipo': self.referencia_tipo,
            'usuario_id': self.usuario_id,
            'fecha_movimiento': self.fecha_movimiento.isoformat() if self.fecha_movimiento else None,
            'observaciones': self.observaciones
        }
        
        if incluir_relaciones:
            if self.paciente:
                data['paciente'] = {
                    'id': self.paciente.id,
                    'nombre_completo': self.paciente.nombre_completo
                }
            
            if self.medico:
                data['medico'] = {
                    'id': self.medico.id,
                    'nombre_completo': self.medico.nombre_completo
                }
            
            if self.usuario:
                data['usuario'] = {
                    'id': self.usuario.id,
                    'nombre_completo': self.usuario.nombre_completo
                }
        
        return data
    
    @staticmethod
    def registrar_ingreso(caja_id, categoria, concepto, monto, forma_pago='efectivo',
                         paciente_id=None, medico_id=None, referencia_id=None,
                         referencia_tipo=None, usuario_id=None, observaciones=None):
        """Método helper para registrar ingreso"""
        return MovimientoCaja(
            caja_id=caja_id,
            tipo='ingreso',
            categoria=categoria,
            concepto=concepto,
            monto=monto,
            forma_pago=forma_pago,
            paciente_id=paciente_id,
            medico_id=medico_id,
            referencia_id=referencia_id,
            referencia_tipo=referencia_tipo,
            usuario_id=usuario_id,
            observaciones=observaciones
        )
    
    @staticmethod
    def registrar_egreso(caja_id, categoria, concepto, monto, forma_pago='efectivo',
                        referencia_id=None, referencia_tipo=None, usuario_id=None,
                        observaciones=None):
        """Método helper para registrar egreso"""
        return MovimientoCaja(
            caja_id=caja_id,
            tipo='egreso',
            categoria=categoria,
            concepto=concepto,
            monto=monto,
            forma_pago=forma_pago,
            referencia_id=referencia_id,
            referencia_tipo=referencia_tipo,
            usuario_id=usuario_id,
            observaciones=observaciones
        )
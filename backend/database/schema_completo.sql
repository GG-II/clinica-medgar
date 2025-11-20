-- ============================================
-- SISTEMA CLÍNICO MEDGAR - BASE DE DATOS COMPLETA
-- Versión: 1.0
-- Fecha: 2024
-- Motor: MySQL 8.0
-- Total de tablas: 32
-- ============================================

-- Crear base de datos
CREATE DATABASE IF NOT EXISTS clinica_medgar
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE clinica_medgar;

-- ============================================
-- MÓDULO 1: AUTENTICACIÓN Y USUARIOS (2 tablas)
-- ============================================

-- Tabla: usuarios
CREATE TABLE usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    rol ENUM('medico', 'enfermera', 'recepcionista', 'administrador') NOT NULL,
    nombre_completo VARCHAR(150) NOT NULL,
    telefono VARCHAR(20),
    activo BOOLEAN DEFAULT TRUE,
    ultimo_acceso DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_rol (rol)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: logs_auditoria
CREATE TABLE logs_auditoria (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    accion VARCHAR(100) NOT NULL,
    tabla_afectada VARCHAR(50),
    registro_id INT,
    detalles TEXT,
    ip_address VARCHAR(45),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    INDEX idx_usuario (usuario_id),
    INDEX idx_timestamp (timestamp),
    INDEX idx_tabla_registro (tabla_afectada, registro_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- MÓDULO 2: PACIENTES E HISTORIA CLÍNICA (8 tablas)
-- ============================================

-- Tabla: pacientes
CREATE TABLE pacientes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre_completo VARCHAR(150) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    sexo ENUM('M', 'F') NOT NULL,
    dpi VARCHAR(20) UNIQUE,
    direccion TEXT,
    municipio VARCHAR(100),
    departamento VARCHAR(100),
    telefono VARCHAR(20),
    telefono_alternativo VARCHAR(20),
    email VARCHAR(100),
    religion VARCHAR(50),
    estado_civil ENUM('soltero', 'casado', 'divorciado', 'viudo', 'union_libre'),
    tiene_igss BOOLEAN DEFAULT FALSE,
    numero_igss VARCHAR(50),
    contacto_emergencia_nombre VARCHAR(150),
    contacto_emergencia_telefono VARCHAR(20),
    contacto_emergencia_relacion VARCHAR(50),
    foto_url VARCHAR(255),
    observaciones TEXT,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_nombre (nombre_completo),
    INDEX idx_dpi (dpi),
    INDEX idx_telefono (telefono),
    INDEX idx_fecha_nacimiento (fecha_nacimiento),
    FULLTEXT idx_busqueda (nombre_completo, dpi, telefono)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: historias_clinicas
CREATE TABLE historias_clinicas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    paciente_id INT NOT NULL,
    tipo_sangre ENUM('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE,
    UNIQUE KEY unique_paciente (paciente_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: consultas
CREATE TABLE consultas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    paciente_id INT NOT NULL,
    medico_id INT NOT NULL,
    fecha_consulta DATETIME NOT NULL,
    motivo_consulta TEXT NOT NULL,
    historia_enfermedad_actual TEXT,
    examen_fisico TEXT,
    diagnostico TEXT,
    plan_tratamiento TEXT,
    observaciones TEXT,
    especialidad ENUM('medicina_general', 'pediatria', 'ginecologia', 'medicina_interna', 'cirugia', 'traumatologia'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE,
    FOREIGN KEY (medico_id) REFERENCES usuarios(id),
    INDEX idx_paciente (paciente_id),
    INDEX idx_medico (medico_id),
    INDEX idx_fecha (fecha_consulta)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: signos_vitales
CREATE TABLE signos_vitales (
    id INT PRIMARY KEY AUTO_INCREMENT,
    consulta_id INT NOT NULL,
    paciente_id INT NOT NULL,
    fecha_registro DATETIME NOT NULL,
    presion_sistolica INT,
    presion_diastolica INT,
    frecuencia_cardiaca INT,
    temperatura DECIMAL(4,2),
    saturacion_oxigeno INT,
    frecuencia_respiratoria INT,
    peso DECIMAL(6,2),
    talla DECIMAL(5,2),
    imc DECIMAL(5,2),
    perimetro_cefalico DECIMAL(5,2),
    frecuencia_cardiaca_fetal INT,
    observaciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (consulta_id) REFERENCES consultas(id) ON DELETE CASCADE,
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE,
    INDEX idx_paciente (paciente_id),
    INDEX idx_fecha (fecha_registro)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: antecedentes
CREATE TABLE antecedentes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    paciente_id INT NOT NULL,
    tipo ENUM('medicos', 'quirurgicos', 'traumaticos', 'alergicos', 'ginecologicos', 'obstetricos') NOT NULL,
    descripcion TEXT NOT NULL,
    fecha_evento DATE,
    relevancia ENUM('alta', 'media', 'baja') DEFAULT 'media',
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE,
    INDEX idx_paciente_tipo (paciente_id, tipo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: vacunas (catálogo)
CREATE TABLE vacunas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    dosis_total INT DEFAULT 1,
    edad_recomendada_meses INT,
    observaciones TEXT,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: aplicaciones_vacunas
CREATE TABLE aplicaciones_vacunas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    paciente_id INT NOT NULL,
    vacuna_id INT NOT NULL,
    numero_dosis INT NOT NULL,
    fecha_aplicacion DATE NOT NULL,
    lote VARCHAR(50),
    aplicada_por VARCHAR(100),
    observaciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE,
    FOREIGN KEY (vacuna_id) REFERENCES vacunas(id),
    INDEX idx_paciente (paciente_id),
    INDEX idx_fecha (fecha_aplicacion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: archivos_paciente
CREATE TABLE archivos_paciente (
    id INT PRIMARY KEY AUTO_INCREMENT,
    paciente_id INT NOT NULL,
    nombre_archivo VARCHAR(255) NOT NULL,
    ruta_archivo VARCHAR(500) NOT NULL,
    tipo_archivo VARCHAR(50),
    categoria ENUM('laboratorios', 'imagenes', 'recetas', 'ekg', 'otros') NOT NULL,
    tamanio_bytes BIGINT,
    descripcion TEXT,
    subido_por INT,
    fecha_subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE,
    FOREIGN KEY (subido_por) REFERENCES usuarios(id),
    INDEX idx_paciente (paciente_id),
    INDEX idx_categoria (categoria)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- MÓDULO 3: AGENDA Y CITAS (3 tablas)
-- ============================================

-- Tabla: tipos_cita
CREATE TABLE tipos_cita (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    descripcion TEXT,
    duracion_minutos INT DEFAULT 20,
    color VARCHAR(7),
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: citas
CREATE TABLE citas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    paciente_id INT NOT NULL,
    medico_id INT NOT NULL,
    tipo_cita_id INT NOT NULL,
    fecha_hora DATETIME NOT NULL,
    duracion_minutos INT DEFAULT 20,
    motivo TEXT,
    estado ENUM('programada', 'confirmada', 'en_curso', 'completada', 'cancelada', 'no_asistio') DEFAULT 'programada',
    notas TEXT,
    es_emergencia BOOLEAN DEFAULT FALSE,
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE,
    FOREIGN KEY (medico_id) REFERENCES usuarios(id),
    FOREIGN KEY (tipo_cita_id) REFERENCES tipos_cita(id),
    FOREIGN KEY (created_by) REFERENCES usuarios(id),
    INDEX idx_medico_fecha (medico_id, fecha_hora),
    INDEX idx_paciente (paciente_id),
    INDEX idx_fecha (fecha_hora),
    INDEX idx_estado (estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: recordatorios
CREATE TABLE recordatorios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cita_id INT NOT NULL,
    tipo ENUM('whatsapp', 'sms', 'email') NOT NULL,
    telefono_destinatario VARCHAR(20),
    mensaje TEXT NOT NULL,
    fecha_envio DATETIME,
    estado ENUM('pendiente', 'enviado', 'fallido', 'confirmado') DEFAULT 'pendiente',
    respuesta_paciente TEXT,
    dias_anticipacion INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (cita_id) REFERENCES citas(id) ON DELETE CASCADE,
    INDEX idx_cita (cita_id),
    INDEX idx_estado (estado),
    INDEX idx_fecha_envio (fecha_envio)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- MÓDULO 4: RECETAS Y MEDICAMENTOS (4 tablas)
-- ============================================

-- Tabla: medicamentos
CREATE TABLE medicamentos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre_generico VARCHAR(200) NOT NULL,
    nombre_comercial VARCHAR(200),
    presentacion VARCHAR(100),
    concentracion VARCHAR(50),
    via_administracion VARCHAR(50),
    interacciones TEXT,
    contraindicaciones TEXT,
    observaciones TEXT,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_nombre_generico (nombre_generico),
    INDEX idx_nombre_comercial (nombre_comercial),
    FULLTEXT idx_busqueda (nombre_generico, nombre_comercial)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: recetas
CREATE TABLE recetas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    paciente_id INT NOT NULL,
    medico_id INT NOT NULL,
    consulta_id INT,
    fecha_emision DATE NOT NULL,
    indicaciones_generales TEXT,
    diagnostico VARCHAR(255),
    activa BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE,
    FOREIGN KEY (medico_id) REFERENCES usuarios(id),
    FOREIGN KEY (consulta_id) REFERENCES consultas(id),
    INDEX idx_paciente (paciente_id),
    INDEX idx_medico (medico_id),
    INDEX idx_fecha (fecha_emision)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: recetas_detalle
CREATE TABLE recetas_detalle (
    id INT PRIMARY KEY AUTO_INCREMENT,
    receta_id INT NOT NULL,
    medicamento_id INT NOT NULL,
    dosis VARCHAR(100) NOT NULL,
    frecuencia VARCHAR(100) NOT NULL,
    duracion VARCHAR(50),
    via_administracion VARCHAR(50),
    indicaciones_especificas TEXT,
    cantidad_prescrita INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (receta_id) REFERENCES recetas(id) ON DELETE CASCADE,
    FOREIGN KEY (medicamento_id) REFERENCES medicamentos(id),
    INDEX idx_receta (receta_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: plantillas_receta
CREATE TABLE plantillas_receta (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    especialidad VARCHAR(50),
    datos_json JSON,
    medico_id INT,
    compartida BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (medico_id) REFERENCES usuarios(id),
    INDEX idx_medico (medico_id),
    INDEX idx_especialidad (especialidad)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- MÓDULO 5: LABORATORIOS (3 tablas)
-- ============================================

-- Tabla: tipos_laboratorio
CREATE TABLE tipos_laboratorio (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(50),
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: laboratorios
CREATE TABLE laboratorios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    paciente_id INT NOT NULL,
    medico_id INT NOT NULL,
    tipo_laboratorio_id INT NOT NULL,
    fecha_solicitud DATE NOT NULL,
    fecha_resultado DATE,
    laboratorio_externo VARCHAR(100),
    resultados JSON,
    interpretacion TEXT,
    observaciones TEXT,
    archivo_url VARCHAR(255),
    estado ENUM('solicitado', 'en_proceso', 'completado', 'cancelado') DEFAULT 'solicitado',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE,
    FOREIGN KEY (medico_id) REFERENCES usuarios(id),
    FOREIGN KEY (tipo_laboratorio_id) REFERENCES tipos_laboratorio(id),
    INDEX idx_paciente (paciente_id),
    INDEX idx_fecha_solicitud (fecha_solicitud),
    INDEX idx_estado (estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: valores_referencia
CREATE TABLE valores_referencia (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tipo_laboratorio_id INT NOT NULL,
    parametro VARCHAR(100) NOT NULL,
    valor_minimo DECIMAL(10,2),
    valor_maximo DECIMAL(10,2),
    unidad VARCHAR(20),
    rango_edad_min INT,
    rango_edad_max INT,
    sexo ENUM('M', 'F', 'ambos') DEFAULT 'ambos',
    observaciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (tipo_laboratorio_id) REFERENCES tipos_laboratorio(id),
    INDEX idx_tipo_parametro (tipo_laboratorio_id, parametro)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- MÓDULO 6: HOSPITALIZACIÓN (5 tablas)
-- ============================================

-- Tabla: camas
CREATE TABLE camas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    numero_cama VARCHAR(10) UNIQUE NOT NULL,
    ubicacion VARCHAR(100),
    estado ENUM('disponible', 'ocupada', 'limpieza', 'mantenimiento') DEFAULT 'disponible',
    observaciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_estado (estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: hospitalizaciones
CREATE TABLE hospitalizaciones (
    id INT PRIMARY KEY AUTO_INCREMENT,
    paciente_id INT NOT NULL,
    cama_id INT NOT NULL,
    medico_responsable_id INT NOT NULL,
    fecha_ingreso DATETIME NOT NULL,
    fecha_egreso DATETIME,
    motivo_ingreso TEXT NOT NULL,
    diagnostico_ingreso TEXT NOT NULL,
    diagnostico_egreso TEXT,
    estado ENUM('activo', 'egresado', 'transferido') DEFAULT 'activo',
    observaciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE,
    FOREIGN KEY (cama_id) REFERENCES camas(id),
    FOREIGN KEY (medico_responsable_id) REFERENCES usuarios(id),
    INDEX idx_paciente (paciente_id),
    INDEX idx_cama (cama_id),
    INDEX idx_estado (estado),
    INDEX idx_fecha_ingreso (fecha_ingreso)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: notas_medicas
CREATE TABLE notas_medicas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    hospitalizacion_id INT NOT NULL,
    medico_id INT NOT NULL,
    tipo_nota ENUM('ingreso', 'evolucion', 'procedimiento', 'operatoria', 'egreso') NOT NULL,
    fecha_hora DATETIME NOT NULL,
    contenido TEXT NOT NULL,
    datos_adicionales JSON,
    firma_digital VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (hospitalizacion_id) REFERENCES hospitalizaciones(id) ON DELETE CASCADE,
    FOREIGN KEY (medico_id) REFERENCES usuarios(id),
    INDEX idx_hospitalizacion (hospitalizacion_id),
    INDEX idx_tipo (tipo_nota),
    INDEX idx_fecha (fecha_hora)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: ordenes_medicas
CREATE TABLE ordenes_medicas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    hospitalizacion_id INT NOT NULL,
    medico_id INT NOT NULL,
    fecha_hora_orden DATETIME NOT NULL,
    tipo_orden ENUM('medicamento', 'dieta', 'signos_vitales', 'laboratorio', 'imagen', 'interconsulta', 'cuidados', 'otro') NOT NULL,
    descripcion TEXT NOT NULL,
    indicaciones TEXT,
    estado ENUM('activa', 'suspendida', 'completada', 'cancelada') DEFAULT 'activa',
    fecha_suspension DATETIME,
    observaciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (hospitalizacion_id) REFERENCES hospitalizaciones(id) ON DELETE CASCADE,
    FOREIGN KEY (medico_id) REFERENCES usuarios(id),
    INDEX idx_hospitalizacion (hospitalizacion_id),
    INDEX idx_estado (estado),
    INDEX idx_fecha (fecha_hora_orden)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: registro_enfermeria
CREATE TABLE registro_enfermeria (
    id INT PRIMARY KEY AUTO_INCREMENT,
    hospitalizacion_id INT NOT NULL,
    enfermera_id INT NOT NULL,
    fecha_hora DATETIME NOT NULL,
    tipo_registro ENUM('signos_vitales', 'medicamento', 'curacion', 'nota', 'otro') NOT NULL,
    descripcion TEXT NOT NULL,
    datos_json JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (hospitalizacion_id) REFERENCES hospitalizaciones(id) ON DELETE CASCADE,
    FOREIGN KEY (enfermera_id) REFERENCES usuarios(id),
    INDEX idx_hospitalizacion (hospitalizacion_id),
    INDEX idx_fecha (fecha_hora)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- MÓDULO 7: FARMACIA E INVENTARIO (5 tablas)
-- ============================================

-- Tabla: proveedores
CREATE TABLE proveedores (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(150) NOT NULL,
    nit VARCHAR(20),
    direccion TEXT,
    telefono VARCHAR(20),
    email VARCHAR(100),
    contacto_nombre VARCHAR(100),
    productos_suministra TEXT,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_nombre (nombre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: productos_farmacia
CREATE TABLE productos_farmacia (
    id INT PRIMARY KEY AUTO_INCREMENT,
    codigo_interno VARCHAR(50) UNIQUE,
    nombre_generico VARCHAR(200) NOT NULL,
    nombre_comercial VARCHAR(200),
    presentacion VARCHAR(100),
    concentracion VARCHAR(50),
    tipo_producto ENUM('medicamento', 'insumo_medico', 'material_curacion', 'solucion_iv', 'equipo') NOT NULL,
    lote VARCHAR(50),
    fecha_vencimiento DATE,
    proveedor_id INT,
    precio_compra DECIMAL(10,2),
    precio_venta DECIMAL(10,2),
    stock_actual INT DEFAULT 0,
    stock_minimo INT DEFAULT 10,
    ubicacion VARCHAR(100),
    requiere_receta BOOLEAN DEFAULT FALSE,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (proveedor_id) REFERENCES proveedores(id),
    INDEX idx_codigo (codigo_interno),
    INDEX idx_stock (stock_actual),
    INDEX idx_vencimiento (fecha_vencimiento),
    FULLTEXT idx_busqueda (nombre_generico, nombre_comercial)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: movimientos_inventario
CREATE TABLE movimientos_inventario (
    id INT PRIMARY KEY AUTO_INCREMENT,
    producto_id INT NOT NULL,
    tipo_movimiento ENUM('entrada', 'salida', 'ajuste', 'devolucion') NOT NULL,
    cantidad INT NOT NULL,
    stock_anterior INT NOT NULL,
    stock_nuevo INT NOT NULL,
    motivo VARCHAR(100),
    referencia_id INT,
    referencia_tipo VARCHAR(50),
    usuario_id INT,
    fecha_movimiento DATETIME DEFAULT CURRENT_TIMESTAMP,
    observaciones TEXT,
    
    FOREIGN KEY (producto_id) REFERENCES productos_farmacia(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    INDEX idx_producto (producto_id),
    INDEX idx_fecha (fecha_movimiento)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: compras
CREATE TABLE compras (
    id INT PRIMARY KEY AUTO_INCREMENT,
    proveedor_id INT NOT NULL,
    numero_factura VARCHAR(50),
    fecha_compra DATE NOT NULL,
    fecha_recepcion DATE,
    subtotal DECIMAL(10,2),
    impuestos DECIMAL(10,2),
    total DECIMAL(10,2) NOT NULL,
    estado ENUM('pendiente', 'recibida', 'parcial', 'cancelada') DEFAULT 'pendiente',
    usuario_id INT,
    observaciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (proveedor_id) REFERENCES proveedores(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    INDEX idx_proveedor (proveedor_id),
    INDEX idx_fecha (fecha_compra),
    INDEX idx_estado (estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: compras_detalle
CREATE TABLE compras_detalle (
    id INT PRIMARY KEY AUTO_INCREMENT,
    compra_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    lote VARCHAR(50),
    fecha_vencimiento DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (compra_id) REFERENCES compras(id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos_farmacia(id),
    INDEX idx_compra (compra_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- MÓDULO 8: FACTURACIÓN Y CAJA (7 tablas)
-- ============================================

-- Tabla: cajas
CREATE TABLE cajas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    fecha_apertura DATETIME NOT NULL,
    fecha_cierre DATETIME,
    monto_inicial DECIMAL(10,2) NOT NULL,
    monto_final DECIMAL(10,2),
    total_ingresos DECIMAL(10,2),
    total_egresos DECIMAL(10,2),
    efectivo_contado DECIMAL(10,2),
    diferencia DECIMAL(10,2),
    estado ENUM('abierta', 'cerrada') DEFAULT 'abierta',
    observaciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    INDEX idx_usuario (usuario_id),
    INDEX idx_fecha_apertura (fecha_apertura),
    INDEX idx_estado (estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: movimientos_caja
CREATE TABLE movimientos_caja (
    id INT PRIMARY KEY AUTO_INCREMENT,
    caja_id INT NOT NULL,
    tipo ENUM('ingreso', 'egreso') NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    concepto TEXT NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    forma_pago ENUM('efectivo', 'transferencia', 'tarjeta', 'cheque') DEFAULT 'efectivo',
    paciente_id INT,
    medico_id INT,
    referencia_id INT,
    referencia_tipo VARCHAR(50),
    usuario_id INT,
    fecha_movimiento DATETIME DEFAULT CURRENT_TIMESTAMP,
    observaciones TEXT,
    
    FOREIGN KEY (caja_id) REFERENCES cajas(id),
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
    FOREIGN KEY (medico_id) REFERENCES usuarios(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    INDEX idx_caja (caja_id),
    INDEX idx_tipo (tipo),
    INDEX idx_fecha (fecha_movimiento)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: convenios
CREATE TABLE convenios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    tipo ENUM('igss', 'seguro_privado', 'empresa') NOT NULL,
    nit VARCHAR(20),
    contacto_nombre VARCHAR(100),
    contacto_telefono VARCHAR(20),
    contacto_email VARCHAR(100),
    porcentaje_cobertura DECIMAL(5,2),
    dias_credito INT DEFAULT 30,
    activo BOOLEAN DEFAULT TRUE,
    observaciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_nombre (nombre),
    INDEX idx_tipo (tipo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: facturas
CREATE TABLE facturas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    numero_factura VARCHAR(50) UNIQUE NOT NULL,
    serie VARCHAR(10),
    uuid_fel VARCHAR(100) UNIQUE,
    paciente_id INT NOT NULL,
    convenio_id INT,
    fecha_emision DATETIME NOT NULL,
    nit_cliente VARCHAR(20),
    nombre_cliente VARCHAR(150),
    direccion_cliente TEXT,
    subtotal DECIMAL(10,2) NOT NULL,
    descuento DECIMAL(10,2) DEFAULT 0,
    impuestos DECIMAL(10,2) DEFAULT 0,
    total DECIMAL(10,2) NOT NULL,
    forma_pago ENUM('efectivo', 'transferencia', 'tarjeta', 'credito') DEFAULT 'efectivo',
    estado ENUM('pendiente', 'pagada', 'anulada', 'credito') DEFAULT 'pendiente',
    certificada_fel BOOLEAN DEFAULT FALSE,
    xml_fel TEXT,
    usuario_id INT,
    observaciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
    FOREIGN KEY (convenio_id) REFERENCES convenios(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    INDEX idx_numero (numero_factura),
    INDEX idx_uuid (uuid_fel),
    INDEX idx_paciente (paciente_id),
    INDEX idx_fecha (fecha_emision),
    INDEX idx_estado (estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: facturas_detalle
CREATE TABLE facturas_detalle (
    id INT PRIMARY KEY AUTO_INCREMENT,
    factura_id INT NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    tipo_servicio VARCHAR(50),
    referencia_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (factura_id) REFERENCES facturas(id) ON DELETE CASCADE,
    INDEX idx_factura (factura_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: cuentas_por_cobrar
CREATE TABLE cuentas_por_cobrar (
    id INT PRIMARY KEY AUTO_INCREMENT,
    factura_id INT NOT NULL,
    paciente_id INT,
    convenio_id INT,
    monto_total DECIMAL(10,2) NOT NULL,
    monto_pagado DECIMAL(10,2) DEFAULT 0,
    saldo_pendiente DECIMAL(10,2) NOT NULL,
    fecha_vencimiento DATE,
    estado ENUM('pendiente', 'parcial', 'pagada', 'vencida') DEFAULT 'pendiente',
    observaciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (factura_id) REFERENCES facturas(id),
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
    FOREIGN KEY (convenio_id) REFERENCES convenios(id),
    INDEX idx_factura (factura_id),
    INDEX idx_paciente (paciente_id),
    INDEX idx_convenio (convenio_id),
    INDEX idx_estado (estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: pagos_cuentas
CREATE TABLE pagos_cuentas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cuenta_id INT NOT NULL,
    monto_pago DECIMAL(10,2) NOT NULL,
    forma_pago ENUM('efectivo', 'transferencia', 'tarjeta', 'cheque') DEFAULT 'efectivo',
    fecha_pago DATETIME NOT NULL,
    numero_recibo VARCHAR(50),
    usuario_id INT,
    observaciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (cuenta_id) REFERENCES cuentas_por_cobrar(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    INDEX idx_cuenta (cuenta_id),
    INDEX idx_fecha (fecha_pago)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- FIN DEL SCHEMA
-- ============================================
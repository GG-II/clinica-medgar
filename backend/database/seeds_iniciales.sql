-- ============================================
-- DATOS INICIALES (SEEDS)
-- Sistema Clínico MEDGAR
-- ============================================

USE clinica_medgar;

-- ============================================
-- CATÁLOGO: Tipos de Cita
-- ============================================

INSERT INTO tipos_cita (nombre, descripcion, duracion_minutos, color) VALUES
('Primera Consulta', 'Primera visita del paciente', 30, '#3B82F6'),
('Reconsulta', 'Consulta de seguimiento', 20, '#10B981'),
('Procedimiento', 'Procedimiento médico programado', 45, '#F59E0B'),
('Control de Embarazo', 'Control prenatal', 30, '#EC4899'),
('Control de Niño Sano', 'Control pediátrico de rutina', 25, '#8B5CF6'),
('Emergencia', 'Consulta de emergencia sin cita', 15, '#EF4444');

-- ============================================
-- CATÁLOGO: Vacunas (Esquema Guatemala)
-- ============================================

INSERT INTO vacunas (nombre, descripcion, dosis_total, edad_recomendada_meses) VALUES
('BCG', 'Bacilo Calmette-Guérin (Tuberculosis)', 1, 0),
('Hepatitis B', 'Hepatitis B', 3, 0),
('Pentavalente', 'DPT + Hepatitis B + Hib', 3, 2),
('Rotavirus', 'Rotavirus', 2, 2),
('Neumococo', 'Neumococo conjugada', 3, 2),
('Polio IPV', 'Polio inactivada', 4, 2),
('Influenza', 'Influenza estacional', 2, 6),
('SRP', 'Sarampión, Rubéola, Paperas', 2, 12),
('Varicela', 'Varicela', 1, 12),
('DPT', 'Difteria, Tos ferina, Tétanos (refuerzo)', 1, 48);

-- ============================================
-- CATÁLOGO: Tipos de Laboratorio
-- ============================================

-- Hematología
INSERT INTO tipos_laboratorio (nombre, categoria) VALUES
('Hemograma Completo', 'Hematología'),
('Velocidad de Sedimentación', 'Hematología'),
('Reticulocitos', 'Hematología'),
('Tiempo de Protrombina (TP)', 'Hematología'),
('Tiempo de Tromboplastina (TPT)', 'Hematología'),
('INR', 'Hematología');

-- Química Sanguínea
INSERT INTO tipos_laboratorio (nombre, categoria) VALUES
('Glucosa en Ayunas', 'Química Sanguínea'),
('Creatinina', 'Química Sanguínea'),
('Urea', 'Química Sanguínea'),
('Ácido Úrico', 'Química Sanguínea'),
('Electrolitos (Na, K, Cl)', 'Química Sanguínea');

-- Función Hepática
INSERT INTO tipos_laboratorio (nombre, categoria) VALUES
('Bilirrubinas', 'Función Hepática'),
('Transaminasas (ALT, AST)', 'Función Hepática'),
('Fosfatasa Alcalina', 'Función Hepática'),
('Albúmina', 'Función Hepática');

-- Perfil Lipídico
INSERT INTO tipos_laboratorio (nombre, categoria) VALUES
('Colesterol Total', 'Perfil Lipídico'),
('HDL', 'Perfil Lipídico'),
('LDL', 'Perfil Lipídico'),
('Triglicéridos', 'Perfil Lipídico');

-- Pruebas Tiroideas
INSERT INTO tipos_laboratorio (nombre, categoria) VALUES
('TSH', 'Pruebas Tiroideas'),
('T3 Libre', 'Pruebas Tiroideas'),
('T4 Libre', 'Pruebas Tiroideas');

-- Diabetes
INSERT INTO tipos_laboratorio (nombre, categoria) VALUES
('Hemoglobina Glucosilada (HbA1c)', 'Diabetes'),
('Curva de Tolerancia a la Glucosa', 'Diabetes');

-- Inmunología
INSERT INTO tipos_laboratorio (nombre, categoria) VALUES
('VIH', 'Inmunología'),
('Hepatitis A', 'Inmunología'),
('Hepatitis B', 'Inmunología'),
('Hepatitis C', 'Inmunología'),
('VDRL', 'Inmunología');

-- Exámenes Generales
INSERT INTO tipos_laboratorio (nombre, categoria) VALUES
('Examen General de Orina', 'Urología'),
('Urocultivo', 'Urología'),
('Coproparasitoscópico', 'Otros'),
('Grupo Sanguíneo y Rh', 'Hematología');

-- ============================================
-- CATÁLOGO: 8 Camas
-- ============================================

INSERT INTO camas (numero_cama, ubicacion, estado) VALUES
('Cama 1', 'Ala Norte - Habitación 101', 'disponible'),
('Cama 2', 'Ala Norte - Habitación 102', 'disponible'),
('Cama 3', 'Ala Norte - Habitación 103', 'disponible'),
('Cama 4', 'Ala Norte - Habitación 104', 'disponible'),
('Cama 5', 'Ala Sur - Habitación 201', 'disponible'),
('Cama 6', 'Ala Sur - Habitación 202', 'disponible'),
('Cama 7', 'Ala Sur - Habitación 203', 'disponible'),
('Cama 8', 'Ala Sur - Habitación 204', 'disponible');

-- ============================================
-- CATÁLOGO: Convenio IGSS
-- ============================================

INSERT INTO convenios (nombre, tipo, porcentaje_cobertura, dias_credito) VALUES
('IGSS - Instituto Guatemalteco de Seguridad Social', 'igss', 100.00, 60);

-- ============================================
-- FIN DE SEEDS
-- ============================================
-- =====================================================
-- SEEDS FASE 3: Citas, Recetas y Laboratorios
-- Sistema Clínica MEDGAR
-- =====================================================

USE clinica_medgar;

-- =====================================================
-- 1. TIPOS DE CITA (6 tipos)
-- =====================================================

INSERT INTO tipos_cita (nombre, descripcion, duracion_minutos, color, activo) VALUES
('Primera Consulta', 'Primera consulta con el médico', 30, '#3B82F6', TRUE),
('Reconsulta', 'Consulta de seguimiento', 20, '#10B981', TRUE),
('Procedimiento', 'Procedimiento médico programado', 45, '#F59E0B', TRUE),
('Control Embarazo', 'Control prenatal', 30, '#EC4899', TRUE),
('Control Niño Sano', 'Control pediátrico de rutina', 25, '#8B5CF6', TRUE),
('Emergencia', 'Atención de emergencia (sin cita previa)', 20, '#EF4444', TRUE);

-- =====================================================
-- 2. TIPOS DE LABORATORIO (35 tipos en 12 categorías)
-- =====================================================

-- CATEGORÍA: Hematología
INSERT INTO tipos_laboratorio (nombre, categoria, descripcion, activo) VALUES
('Hemograma Completo', 'Hematología', 'Conteo de células sanguíneas completo', TRUE),
('Velocidad de Sedimentación (VSG)', 'Hematología', 'Indicador de inflamación', TRUE),
('Tiempos de Coagulación', 'Hematología', 'TP, TPT, INR', TRUE),
('Grupo Sanguíneo y RH', 'Hematología', 'Determinación de grupo y factor', TRUE);

-- CATEGORÍA: Química Sanguínea
INSERT INTO tipos_laboratorio (nombre, categoria, descripcion, activo) VALUES
('Glucosa en Ayunas', 'Química Sanguínea', 'Nivel de azúcar en sangre', TRUE),
('Creatinina', 'Química Sanguínea', 'Función renal', TRUE),
('Urea', 'Química Sanguínea', 'Producto final del metabolismo proteico', TRUE),
('Ácido Úrico', 'Química Sanguínea', 'Relacionado con gota', TRUE),
('Electrolitos (Na, K, Cl)', 'Química Sanguínea', 'Sodio, Potasio, Cloro', TRUE);

-- CATEGORÍA: Función Hepática
INSERT INTO tipos_laboratorio (nombre, categoria, descripcion, activo) VALUES
('Transaminasas (ALT, AST)', 'Función Hepática', 'Enzimas hepáticas', TRUE),
('Bilirrubinas', 'Función Hepática', 'Total, directa e indirecta', TRUE),
('Fosfatasa Alcalina', 'Función Hepática', 'Enzima relacionada con hígado y huesos', TRUE),
('Albúmina', 'Función Hepática', 'Proteína producida por el hígado', TRUE);

-- CATEGORÍA: Perfil Lipídico
INSERT INTO tipos_laboratorio (nombre, categoria, descripcion, activo) VALUES
('Perfil Lipídico Completo', 'Perfil Lipídico', 'Colesterol total, HDL, LDL, Triglicéridos', TRUE),
('Colesterol Total', 'Perfil Lipídico', 'Nivel total de colesterol', TRUE),
('Triglicéridos', 'Perfil Lipídico', 'Tipo de grasa en sangre', TRUE);

-- CATEGORÍA: Pruebas Tiroideas
INSERT INTO tipos_laboratorio (nombre, categoria, descripcion, activo) VALUES
('TSH', 'Pruebas Tiroideas', 'Hormona estimulante de tiroides', TRUE),
('T3 y T4 Libre', 'Pruebas Tiroideas', 'Hormonas tiroideas', TRUE);

-- CATEGORÍA: Diabetes
INSERT INTO tipos_laboratorio (nombre, categoria, descripcion, activo) VALUES
('Hemoglobina Glucosilada (HbA1c)', 'Diabetes', 'Control de diabetes últimos 3 meses', TRUE),
('Curva de Tolerancia a la Glucosa', 'Diabetes', 'Prueba de tolerancia oral', TRUE);

-- CATEGORÍA: Marcadores Tumorales
INSERT INTO tipos_laboratorio (nombre, categoria, descripcion, activo) VALUES
('PSA', 'Marcadores Tumorales', 'Antígeno prostático específico', TRUE),
('CA 125', 'Marcadores Tumorales', 'Marcador de cáncer ovárico', TRUE),
('CA 19-9', 'Marcadores Tumorales', 'Marcador de cáncer pancreático', TRUE),
('AFP', 'Marcadores Tumorales', 'Alfafetoproteína', TRUE);

-- CATEGORÍA: Inmunología
INSERT INTO tipos_laboratorio (nombre, categoria, descripcion, activo) VALUES
('VIH (ELISA)', 'Inmunología', 'Detección de anticuerpos VIH', TRUE),
('Hepatitis B (HBsAg)', 'Inmunología', 'Antígeno de superficie hepatitis B', TRUE),
('Hepatitis C (Anti-HCV)', 'Inmunología', 'Anticuerpos hepatitis C', TRUE),
('VDRL', 'Inmunología', 'Prueba de sífilis', TRUE);

-- CATEGORÍA: Orina y Heces
INSERT INTO tipos_laboratorio (nombre, categoria, descripcion, activo) VALUES
('Examen General de Orina', 'Orina y Heces', 'Análisis físico, químico y microscópico', TRUE),
('Urocultivo', 'Orina y Heces', 'Cultivo de orina', TRUE),
('Coproparasitoscópico', 'Orina y Heces', 'Búsqueda de parásitos en heces', TRUE),
('Sangre Oculta en Heces', 'Orina y Heces', 'Detección de sangre microscópica', TRUE);

-- CATEGORÍA: Microbiología
INSERT INTO tipos_laboratorio (nombre, categoria, descripcion, activo) VALUES
('Hemocultivo', 'Microbiología', 'Cultivo de sangre', TRUE),
('Antibiograma', 'Microbiología', 'Sensibilidad a antibióticos', TRUE);

-- CATEGORÍA: Función Renal
INSERT INTO tipos_laboratorio (nombre, categoria, descripcion, activo) VALUES
('Depuración de Creatinina', 'Función Renal', 'Filtrado glomerular', TRUE);

-- =====================================================
-- 3. VALORES DE REFERENCIA (ejemplos principales)
-- =====================================================

-- Hemograma Completo
INSERT INTO valores_referencia (tipo_laboratorio_id, parametro, valor_minimo, valor_maximo, unidad, sexo, rango_edad_min, rango_edad_max) VALUES
(1, 'hemoglobina', 13.0, 17.0, 'g/dL', 'M', 18, NULL),
(1, 'hemoglobina', 12.0, 16.0, 'g/dL', 'F', 18, NULL),
(1, 'leucocitos', 4000, 11000, '/mm³', 'ambos', 18, NULL),
(1, 'plaquetas', 150000, 450000, '/mm³', 'ambos', 18, NULL),
(1, 'hematocrito', 40, 54, '%', 'M', 18, NULL),
(1, 'hematocrito', 37, 47, '%', 'F', 18, NULL);

-- Glucosa
INSERT INTO valores_referencia (tipo_laboratorio_id, parametro, valor_minimo, valor_maximo, unidad, sexo, rango_edad_min, rango_edad_max) VALUES
(5, 'glucosa', 70, 100, 'mg/dL', 'ambos', 18, NULL);

-- Creatinina
INSERT INTO valores_referencia (tipo_laboratorio_id, parametro, valor_minimo, valor_maximo, unidad, sexo, rango_edad_min, rango_edad_max) VALUES
(6, 'creatinina', 0.7, 1.3, 'mg/dL', 'M', 18, NULL),
(6, 'creatinina', 0.6, 1.1, 'mg/dL', 'F', 18, NULL);

-- Ácido Úrico
INSERT INTO valores_referencia (tipo_laboratorio_id, parametro, valor_minimo, valor_maximo, unidad, sexo, rango_edad_min, rango_edad_max) VALUES
(8, 'acido_urico', 3.4, 7.0, 'mg/dL', 'M', 18, NULL),
(8, 'acido_urico', 2.4, 6.0, 'mg/dL', 'F', 18, NULL);

-- Colesterol Total
INSERT INTO valores_referencia (tipo_laboratorio_id, parametro, valor_minimo, valor_maximo, unidad, sexo, rango_edad_min, rango_edad_max) VALUES
(15, 'colesterol_total', 0, 200, 'mg/dL', 'ambos', 18, NULL);

-- Triglicéridos
INSERT INTO valores_referencia (tipo_laboratorio_id, parametro, valor_minimo, valor_maximo, unidad, sexo, rango_edad_min, rango_edad_max) VALUES
(17, 'trigliceridos', 0, 150, 'mg/dL', 'ambos', 18, NULL);

-- TSH
INSERT INTO valores_referencia (tipo_laboratorio_id, parametro, valor_minimo, valor_maximo, unidad, sexo, rango_edad_min, rango_edad_max) VALUES
(18, 'tsh', 0.4, 4.0, 'mIU/L', 'ambos', 18, NULL);

-- Hemoglobina Glucosilada
INSERT INTO valores_referencia (tipo_laboratorio_id, parametro, valor_minimo, valor_maximo, unidad, sexo, rango_edad_min, rango_edad_max) VALUES
(20, 'hba1c', 0, 5.6, '%', 'ambos', 18, NULL);

-- =====================================================
-- 4. MEDICAMENTOS (50 medicamentos comunes en Guatemala)
-- =====================================================

INSERT INTO medicamentos (nombre_generico, nombre_comercial, presentacion, concentracion, via_administracion, activo) VALUES
-- Analgésicos y Antiinflamatorios
('Paracetamol', 'Tylenol', 'Tableta', '500mg', 'Oral', TRUE),
('Ibuprofeno', 'Advil', 'Tableta', '400mg', 'Oral', TRUE),
('Naproxeno', 'Flanax', 'Tableta', '250mg', 'Oral', TRUE),
('Diclofenaco', 'Voltaren', 'Tableta', '50mg', 'Oral', TRUE),
('Ketorolaco', 'Dolac', 'Ampolla', '30mg/ml', 'Intramuscular', TRUE),

-- Antibióticos
('Amoxicilina', 'Amoxil', 'Cápsula', '500mg', 'Oral', TRUE),
('Amoxicilina + Ácido Clavulánico', 'Augmentin', 'Tableta', '875mg/125mg', 'Oral', TRUE),
('Azitromicina', 'Zitromax', 'Tableta', '500mg', 'Oral', TRUE),
('Ciprofloxacina', 'Cipro', 'Tableta', '500mg', 'Oral', TRUE),
('Cefalexina', 'Keflex', 'Cápsula', '500mg', 'Oral', TRUE),
('Trimetoprim + Sulfametoxazol', 'Bactrim', 'Tableta', '160mg/800mg', 'Oral', TRUE),

-- Antihipertensivos
('Losartán', 'Cozaar', 'Tableta', '50mg', 'Oral', TRUE),
('Enalapril', 'Vasotec', 'Tableta', '10mg', 'Oral', TRUE),
('Amlodipino', 'Norvasc', 'Tableta', '5mg', 'Oral', TRUE),
('Hidroclorotiazida', 'Microzide', 'Tableta', '25mg', 'Oral', TRUE),

-- Antidiabéticos
('Metformina', 'Glucophage', 'Tableta', '850mg', 'Oral', TRUE),
('Glibenclamida', 'Daonil', 'Tableta', '5mg', 'Oral', TRUE),
('Insulina NPH', 'Humulin N', 'Frasco', '100UI/ml', 'Subcutánea', TRUE),

-- Antiácidos y Gastroprotectores
('Omeprazol', 'Prilosec', 'Cápsula', '20mg', 'Oral', TRUE),
('Ranitidina', 'Zantac', 'Tableta', '150mg', 'Oral', TRUE),
('Hidróxido de Aluminio + Magnesio', 'Maalox', 'Suspensión', '200ml', 'Oral', TRUE),

-- Antihistamínicos
('Loratadina', 'Claritin', 'Tableta', '10mg', 'Oral', TRUE),
('Cetirizina', 'Zyrtec', 'Tableta', '10mg', 'Oral', TRUE),
('Difenhidramina', 'Benadryl', 'Tableta', '25mg', 'Oral', TRUE),

-- Broncodilatadores
('Salbutamol', 'Ventolin', 'Inhalador', '100mcg', 'Inhalada', TRUE),
('Teofilina', 'Theo-24', 'Tableta', '300mg', 'Oral', TRUE),

-- Corticoides
('Prednisona', 'Deltasone', 'Tableta', '5mg', 'Oral', TRUE),
('Dexametasona', 'Decadron', 'Ampolla', '4mg/ml', 'Intramuscular', TRUE),
('Betametasona', 'Celestone', 'Crema', '0.05%', 'Tópica', TRUE),

-- Vitaminas y Suplementos
('Ácido Fólico', 'Folvite', 'Tableta', '5mg', 'Oral', TRUE),
('Complejo B', 'Neurobion', 'Ampolla', '3ml', 'Intramuscular', TRUE),
('Hierro', 'Feosol', 'Tableta', '325mg', 'Oral', TRUE),
('Vitamina C', 'Redoxon', 'Tableta Efervescente', '1000mg', 'Oral', TRUE),

-- Antieméticos
('Metoclopramida', 'Reglan', 'Tableta', '10mg', 'Oral', TRUE),
('Dimenhidrinato', 'Dramamine', 'Tableta', '50mg', 'Oral', TRUE),

-- Antipiréticos
('Dipirona', 'Novalgin', 'Ampolla', '1g/2ml', 'Intramuscular', TRUE),

-- Antiespasmódicos
('Hioscina', 'Buscapina', 'Tableta', '10mg', 'Oral', TRUE),

-- Anticonceptivos
('Levonorgestrel + Etinilestradiol', 'Microgynon', 'Tableta', '0.15mg/0.03mg', 'Oral', TRUE),

-- Antiparasitarios
('Albendazol', 'Zentel', 'Tableta', '400mg', 'Oral', TRUE),
('Metronidazol', 'Flagyl', 'Tableta', '500mg', 'Oral', TRUE),

-- Anticoagulantes
('Ácido Acetilsalicílico', 'Aspirina', 'Tableta', '100mg', 'Oral', TRUE),

-- Diuréticos
('Furosemida', 'Lasix', 'Tableta', '40mg', 'Oral', TRUE),

-- Ansiolíticos
('Alprazolam', 'Xanax', 'Tableta', '0.25mg', 'Oral', TRUE),
('Clonazepam', 'Rivotril', 'Tableta', '2mg', 'Oral', TRUE),

-- Anticonvulsivantes
('Fenitoína', 'Dilantin', 'Tableta', '100mg', 'Oral', TRUE),
('Ácido Valproico', 'Depakote', 'Tableta', '500mg', 'Oral', TRUE),

-- Antimicóticos
('Fluconazol', 'Diflucan', 'Cápsula', '150mg', 'Oral', TRUE),
('Clotrimazol', 'Canesten', 'Crema', '1%', 'Tópica', TRUE);

-- =====================================================
-- RESUMEN DE DATOS INSERTADOS
-- =====================================================
-- ✅ 6 tipos de cita
-- ✅ 35 tipos de laboratorio (12 categorías)
-- ✅ 15 valores de referencia (ejemplos principales)
-- ✅ 50 medicamentos comunes en Guatemala
-- =====================================================

SELECT 'Seeds Fase 3 ejecutados exitosamente' AS mensaje;
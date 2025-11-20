-- =====================================================
-- SEEDS FASE 4: Hospitalización, Farmacia, Facturación
-- =====================================================

USE clinica_medgar;

-- =====================================================
-- 1. CAMAS (8 camas)
-- =====================================================

INSERT INTO camas (numero_cama, ubicacion, estado, observaciones) VALUES
('CAMA-01', 'Sala General - Área A', 'disponible', 'Cama con monitor'),
('CAMA-02', 'Sala General - Área A', 'disponible', NULL),
('CAMA-03', 'Sala General - Área B', 'disponible', NULL),
('CAMA-04', 'Sala General - Área B', 'disponible', NULL),
('CAMA-05', 'Sala Privada 1', 'disponible', 'Incluye baño privado'),
('CAMA-06', 'Sala Privada 2', 'disponible', 'Incluye baño privado'),
('CAMA-07', 'Observación', 'disponible', 'Área de observación'),
('CAMA-08', 'Observación', 'disponible', 'Área de observación');

-- =====================================================
-- 2. PROVEEDORES (5 proveedores)
-- =====================================================

INSERT INTO proveedores (nombre, nit, direccion, telefono, email, contacto_nombre, productos_suministra, activo) VALUES
('Distribuidora Farmacéutica del Centro', '1234567-8', 'Zona 1, Ciudad de Guatemala', '2222-3333', 'ventas@distfarmaceutica.com', 'Juan Pérez', 'Medicamentos genéricos y de marca', TRUE),
('Insumos Médicos Guatemala', '2345678-9', 'Zona 10, Ciudad de Guatemala', '2333-4444', 'info@insumed.gt', 'María López', 'Insumos médicos, gasas, jeringas', TRUE),
('Laboratorios Nacionales S.A.', '3456789-0', 'Zona 12, Ciudad de Guatemala', '2444-5555', 'contacto@labnacionales.com', 'Carlos Ramírez', 'Medicamentos de fabricación nacional', TRUE),
('Importadora de Equipos Médicos', '4567890-1', 'Zona 4, Ciudad de Guatemala', '2555-6666', 'ventas@imequimed.com', 'Ana García', 'Equipos médicos y soluciones IV', TRUE),
('Farmacéutica Internacional', '5678901-2', 'Zona 15, Ciudad de Guatemala', '2666-7777', 'info@farminter.gt', 'Luis Hernández', 'Medicamentos importados', TRUE);

-- =====================================================
-- 3. PRODUCTOS DE FARMACIA (50 productos)
-- =====================================================

-- Medicamentos
INSERT INTO productos_farmacia (codigo_interno, nombre_generico, nombre_comercial, presentacion, concentracion, tipo_producto, lote, fecha_vencimiento, proveedor_id, precio_compra, precio_venta, stock_actual, stock_minimo, ubicacion, requiere_receta, activo) VALUES
('MED-001', 'Paracetamol', 'Tylenol', 'Tabletas', '500mg', 'medicamento', 'LOT2024A', '2026-12-31', 1, 2.50, 5.00, 200, 50, 'Estante A1', FALSE, TRUE),
('MED-002', 'Ibuprofeno', 'Advil', 'Tabletas', '400mg', 'medicamento', 'LOT2024B', '2026-06-30', 1, 3.00, 6.00, 150, 40, 'Estante A2', FALSE, TRUE),
('MED-003', 'Amoxicilina', 'Amoxil', 'Cápsulas', '500mg', 'medicamento', 'LOT2024C', '2025-12-31', 1, 5.00, 10.00, 100, 30, 'Estante A3', TRUE, TRUE),
('MED-004', 'Omeprazol', 'Prilosec', 'Cápsulas', '20mg', 'medicamento', 'LOT2024D', '2026-03-31', 2, 4.00, 8.00, 120, 35, 'Estante A4', FALSE, TRUE),
('MED-005', 'Losartán', 'Cozaar', 'Tabletas', '50mg', 'medicamento', 'LOT2024E', '2025-09-30', 3, 6.00, 12.00, 80, 25, 'Estante B1', TRUE, TRUE),
('MED-006', 'Metformina', 'Glucophage', 'Tabletas', '850mg', 'medicamento', 'LOT2024F', '2026-01-31', 3, 3.50, 7.00, 150, 40, 'Estante B2', TRUE, TRUE),
('MED-007', 'Atorvastatina', 'Lipitor', 'Tabletas', '20mg', 'medicamento', 'LOT2024G', '2025-11-30', 5, 8.00, 16.00, 60, 20, 'Estante B3', TRUE, TRUE),
('MED-008', 'Loratadina', 'Claritin', 'Tabletas', '10mg', 'medicamento', 'LOT2024H', '2026-08-31', 1, 2.00, 4.00, 180, 50, 'Estante B4', FALSE, TRUE),
('MED-009', 'Diclofenaco', 'Voltaren', 'Tabletas', '50mg', 'medicamento', 'LOT2024I', '2025-10-31', 2, 3.50, 7.00, 90, 30, 'Estante C1', FALSE, TRUE),
('MED-010', 'Cetirizina', 'Zyrtec', 'Tabletas', '10mg', 'medicamento', 'LOT2024J', '2026-05-31', 1, 2.50, 5.00, 140, 40, 'Estante C2', FALSE, TRUE);

-- Insumos Médicos
INSERT INTO productos_farmacia (codigo_interno, nombre_generico, nombre_comercial, presentacion, concentracion, tipo_producto, lote, fecha_vencimiento, proveedor_id, precio_compra, precio_venta, stock_actual, stock_minimo, ubicacion, requiere_receta, activo) VALUES
('INS-001', 'Jeringas desechables', 'Mediject', 'Caja x 100', '5ml', 'insumo_medico', NULL, NULL, 2, 25.00, 50.00, 50, 10, 'Bodega A', FALSE, TRUE),
('INS-002', 'Jeringas desechables', 'Mediject', 'Caja x 100', '10ml', 'insumo_medico', NULL, NULL, 2, 30.00, 60.00, 40, 10, 'Bodega A', FALSE, TRUE),
('INS-003', 'Agujas hipodérmicas', 'BD', 'Caja x 100', '21G', 'insumo_medico', NULL, NULL, 2, 20.00, 40.00, 60, 15, 'Bodega A', FALSE, TRUE),
('INS-004', 'Guantes de látex', 'SafeHands', 'Caja x 100', 'Talla M', 'insumo_medico', NULL, '2026-12-31', 2, 35.00, 70.00, 80, 20, 'Bodega B', FALSE, TRUE),
('INS-005', 'Guantes de látex', 'SafeHands', 'Caja x 100', 'Talla L', 'insumo_medico', NULL, '2026-12-31', 2, 35.00, 70.00, 70, 20, 'Bodega B', FALSE, TRUE),
('INS-006', 'Mascarillas quirúrgicas', 'MediMask', 'Caja x 50', 'Desechables', 'insumo_medico', NULL, NULL, 2, 15.00, 30.00, 100, 25, 'Bodega B', FALSE, TRUE),
('INS-007', 'Alcohol gel', 'CleanHands', 'Galón', '70%', 'insumo_medico', NULL, '2025-12-31', 2, 40.00, 80.00, 30, 10, 'Bodega C', FALSE, TRUE),
('INS-008', 'Termómetros digitales', 'TempCheck', 'Unidad', 'Digital', 'insumo_medico', NULL, NULL, 4, 50.00, 100.00, 20, 5, 'Equipo', FALSE, TRUE);

-- Material de Curación
INSERT INTO productos_farmacia (codigo_interno, nombre_generico, nombre_comercial, presentacion, concentracion, tipo_producto, lote, fecha_vencimiento, proveedor_id, precio_compra, precio_venta, stock_actual, stock_minimo, ubicacion, requiere_receta, activo) VALUES
('MAT-001', 'Gasas estériles', 'MediGauze', 'Paquete x 10', '10x10cm', 'material_curacion', NULL, NULL, 2, 10.00, 20.00, 150, 40, 'Bodega C', FALSE, TRUE),
('MAT-002', 'Vendas elásticas', 'FlexBand', 'Rollo', '10cm x 5m', 'material_curacion', NULL, NULL, 2, 8.00, 16.00, 100, 30, 'Bodega C', FALSE, TRUE),
('MAT-003', 'Esparadrapo', 'StickyTape', 'Rollo', '2.5cm x 5m', 'material_curacion', NULL, NULL, 2, 5.00, 10.00, 120, 35, 'Bodega C', FALSE, TRUE),
('MAT-004', 'Algodón', 'SoftCotton', 'Bolsa', '500g', 'material_curacion', NULL, NULL, 2, 15.00, 30.00, 80, 20, 'Bodega C', FALSE, TRUE),
('MAT-005', 'Curitas adhesivas', 'Band-Aid', 'Caja x 100', 'Variadas', 'material_curacion', NULL, NULL, 2, 12.00, 25.00, 90, 25, 'Bodega C', FALSE, TRUE);

-- Soluciones IV
INSERT INTO productos_farmacia (codigo_interno, nombre_generico, nombre_comercial, presentacion, concentracion, tipo_producto, lote, fecha_vencimiento, proveedor_id, precio_compra, precio_venta, stock_actual, stock_minimo, ubicacion, requiere_receta, activo) VALUES
('SOL-001', 'Solución Salina', 'NaCl 0.9%', 'Bolsa', '1000ml', 'solucion_iv', 'LOT2024K', '2025-12-31', 4, 15.00, 30.00, 100, 25, 'Refrigerador A', TRUE, TRUE),
('SOL-002', 'Solución Glucosada', 'Dextrosa 5%', 'Bolsa', '1000ml', 'solucion_iv', 'LOT2024L', '2025-10-31', 4, 18.00, 36.00, 80, 20, 'Refrigerador A', TRUE, TRUE),
('SOL-003', 'Solución Hartmann', 'Ringer Lactato', 'Bolsa', '1000ml', 'solucion_iv', 'LOT2024M', '2025-11-30', 4, 20.00, 40.00, 70, 20, 'Refrigerador A', TRUE, TRUE);

-- =====================================================
-- 4. CONVENIOS (2 convenios iniciales)
-- =====================================================

INSERT INTO convenios (nombre, tipo, nit, contacto_nombre, contacto_telefono, contacto_email, porcentaje_cobertura, dias_credito, activo, observaciones) VALUES
('IGSS - Instituto Guatemalteco de Seguridad Social', 'igss', '123456-7', 'Departamento Pagos', '2412-1212', 'pagos@igss.gob.gt', 100.00, 60, TRUE, 'Convenio estándar IGSS'),
('Seguros El Roble', 'seguro_privado', '234567-8', 'Ana Martínez', '2333-4444', 'ana.martinez@segurosroble.com', 80.00, 30, TRUE, 'Copago 20% paciente');

-- =====================================================
-- MENSAJE FINAL
-- =====================================================

SELECT '✅ Seeds Fase 4 insertados correctamente' as mensaje;
SELECT 'Resumen:' as '';
SELECT CONCAT('  - Camas: ', COUNT(*), ' registradas') FROM camas;
SELECT CONCAT('  - Proveedores: ', COUNT(*), ' registrados') FROM proveedores;
SELECT CONCAT('  - Productos Farmacia: ', COUNT(*), ' registrados') FROM productos_farmacia;
SELECT CONCAT('  - Convenios: ', COUNT(*), ' registrados') FROM convenios;
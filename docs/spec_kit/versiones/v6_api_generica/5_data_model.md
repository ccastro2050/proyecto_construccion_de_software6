# Modelo de datos — Versión 6: la misma bdfacturas, descubierta en runtime

> La v6 no agrega tablas ni motores: agrega una FORMA DE ACCESO. Las 12
> tablas de bdfacturas (idénticas en los tres motores desde la v5) dejan
> de necesitar una rebanada de código por tabla: la API genérica las
> descubre preguntándole al CATÁLOGO del motor.

---

## 1. El catálogo: la tabla de las tablas

Cada motor expone sus metadatos (INFORMATION_SCHEMA en los tres, con
acentos propios). El componente los usa para DOS cosas:

1. **Descubrir** columnas y tipos → las filas viajan como diccionario
   columna→valor y `/api/estructuras` las expone como endpoint.
2. **Validar** nombres de tabla/columna ANTES de armar SQL — la defensa
   contra inyección cuando los identificadores llegan por la URL (los
   VALORES siempre van parametrizados, como en todo el curso).

## 2. Qué gana cobertura con la genérica

| Tablas | En api_facturas (v1-v5) | En la genérica (v6) |
|---|---|---|
| producto, persona, empresa, cliente, vendedor | rebanadas tipadas | también, como diccionarios |
| factura + productosporfactura | 4 endpoints vía SPs | los MISMOS SPs vía `/api/procedimientos/ejecutarsp` |
| **usuario, rol, ruta, rol_usuario, rutarol** | **sin endpoints** (decisión de la v3) | **CRUD completo** — la deuda, cobrada |

## 3. Los SPs, ahora por nombre

Los scripts de la BD traen desde la v1 los SPs de factura Y los de
usuarios/roles/permisos (`crear_usuario_con_roles`,
`verificar_acceso_ruta`, `listar_rutarol`…). La API por-entidad solo
llamó los de factura; `/api/procedimientos/ejecutarsp` los abre TODOS
por nombre — el terreno RBAC que usará el front (v7).

## 4. Seguridad sobre los datos

- `usuario.contrasena`: BCrypt al escribir (`?camposEncriptar=`), y la
  verificación compara SIN devolver el hash.
- **Tablas prohibidas** (`TablasProhibidas` en appsettings): la lista
  que corta con 403 — el mecanismo para vetar tablas sensibles cuando el
  sistema crezca.

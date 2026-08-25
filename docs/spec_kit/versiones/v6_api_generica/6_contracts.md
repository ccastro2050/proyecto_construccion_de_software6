# Contratos — Versión 6: los endpoints del componente nuevo

> `api_facturas` conserva sus 51 endpoints TAL CUAL (solo su diagnóstico
> dice `"version": "v6"`). Los contratos del componente nuevo viven, con
> ejemplos completos, en sus manuales:
> **[GUIA_USO_ENTIDADES](../../../../api_generica_csharp/GUIA_USO_ENTIDADES.md)** y
> **[GUIA_USO_PROCEDIMIENTOS](../../../../api_generica_csharp/GUIA_USO_PROCEDIMIENTOS.md)**
> (más `ApiGenericaCsharp.http` y el Swagger en :8048/swagger).
> Aquí, el mapa de grupos:

---

## Base: `http://localhost:8048`

| Grupo | Endpoints | Notas |
|---|---|---|
| **Diagnóstico** | `GET /api/diagnostico/conexion` | motor activo + estado de conexión |
| **Autenticación** | `POST /api/autenticacion/token` | body: `{tabla, campoUsuario, campoContrasena, usuario, contrasena}` → 200 `{token…}` · 401 · 404 |
| **Entidades** | `GET /api/{tabla}` (**JWT**) · `GET /api/{tabla}/{id}?...` · `POST /api/{tabla}` · `PUT/PATCH /api/{tabla}/...` · `DELETE /api/{tabla}/...` | filas como diccionario columna→valor; `?camposEncriptar=col1,col2` hashea con BCrypt al escribir; `?limite=` y `?esquema=` en lecturas |
| | `POST /api/{tabla}/verificar-contrasena` | 200 válida · 401 incorrecta · 404 no existe |
| **Consultas** | `POST /api/consultas` | SELECT parametrizado de solo lectura, parámetros nombrados |
| **Procedimientos** | `POST /api/procedimientos/ejecutarsp` | `{nombreSP, …parámetros…}` — ejecuta cualquier SP de la BD y devuelve su resultado |
| **Estructuras** | `GET /api/estructuras/…` | tablas y columnas del catálogo (el descubrir-en-runtime, expuesto) |

## Los códigos

200 · 204 vacío · 400 parámetros/body · **401 sin token o credenciales
malas** · **403 tabla prohibida** · 404 tabla/fila inexistente · 500 el
motor (el `detalle` redacta según el dialecto — igual que en
api_facturas).

## El contraste con api_facturas (la tabla que resume el curso)

| | api_facturas (:8047) | api_generica (:8048) |
|---|---|---|
| Rutas | una por entidad | `/api/{tabla}` para todas |
| Validación | tipada en la frontera (422 con errores[]) | contra el catálogo, en runtime |
| Filas | clases modelo | diccionarios columna→valor |
| Cobertura | 6 entidades + factura | las 12 tablas + cualquier SP |
| Seguridad | abierta (por ahora) | JWT en lecturas + BCrypt por campo + tablas prohibidas |
| Motor | interruptor MOTOR_BD | el MISMO interruptor |

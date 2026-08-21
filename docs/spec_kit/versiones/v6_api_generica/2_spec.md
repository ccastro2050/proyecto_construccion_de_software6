# Especificación — Versión 6: la API genérica de plataforma

> **Versión 6** del desarrollo incremental ([mapa de versiones](../0_mapa_versiones.md)).
> Rige la constitución: [../../1_constitution.md](../../1_constitution.md).
> **Acumulativa:** `api_facturas` (v1-v5) no se toca — sus 51 endpoints y
> su regresión triple siguen vigentes tal cual. La v6 SUMA un componente.
>
> | Documento de esta versión | Contenido |
> |---|---|
> | **2_spec.md** (este) | QUÉ agrega la v6 y sus criterios de aceptación |
> | [3_plan.md](3_plan.md) | CÓMO: el componente, sus capas y su integración |
> | [4_research.md](4_research.md) | Decisiones y alternativas *(lectura opcional)* |
> | [5_data_model.md](5_data_model.md) | La misma bdfacturas, ahora descubierta en runtime |
> | [6_contracts.md](6_contracts.md) | Los grupos de endpoints del componente nuevo |
> | [7_quickstart.md](7_quickstart.md) | Smoke test: JWT, CRUD genérico, consultas y SPs |
> | [8_tasks.md](8_tasks.md) | Orden de construcción por fases verificables |
> | [GUIA_IA6.md](GUIA_IA6.md) | Cómo abordar esta versión con IA |

---

## 1. Propósito de la v6

**El contraste de las dos filosofías.** El curso construyó durante cinco
versiones una API **por entidad**: una ruta por tabla, peticiones tipadas
por verbo, validación en la frontera. La v6 pone al lado la otra
filosofía: una **API genérica de plataforma** (`api_generica_csharp`,
puerto **8043**) donde `/api/{tabla}` opera CUALQUIER tabla descubriendo
sus columnas en runtime — filas como diccionario columna→valor.

Ninguna es "mejor": la por-entidad da contratos exactos y validación
rica; la genérica da cobertura total sin escribir una rebanada por tabla
(las 12 tablas quedan operables — incluidas usuario, rol, ruta y los
puentes, que la API por-entidad de este curso nunca cubrió: **esa
decisión, tomada en la v3, se cobra aquí**). Verlas convivir contra los
MISMOS tres motores es la lección de arquitectura del curso.

## 2. Alcance

**Incluye:** el componente `api_generica_csharp/` (referencia PROVISTA
del curso, como la BD) integrado al compose: CRUD genérico
`/api/{tabla}` · **autenticación JWT** (`/api/autenticacion/token`,
login contra cualquier tabla de usuarios) · **encriptación BCrypt de
campos** (`?camposEncriptar=`) · **consultas SELECT parametrizadas**
(`/api/consultas`) · **ejecución de procedimientos almacenados**
(`/api/procedimientos/ejecutarsp`) · **exploración de estructuras**
(`/api/estructuras`) · política de tablas prohibidas · selección de
motor por configuración (el MISMO interruptor `MOTOR_BD` gobierna las
dos APIs).

**No incluye:** el front (v7) · cambios en `api_facturas` (ninguno — el
diff lo demuestra) · protección JWT de `api_facturas` (cada API tiene su
modelo de seguridad; la genérica protege sus lecturas).

## 3. Requisitos funcionales (los grupos del componente)

1. **Entidades** — `GET/POST/PUT/PATCH/DELETE /api/{tabla}`: CRUD sobre
   cualquier tabla no prohibida; `GET` exige JWT (`[Authorize]`);
   `?camposEncriptar=col1,col2` hashea con BCrypt al escribir;
   `POST /api/{tabla}/verificar-contrasena` verifica contra el hash.
2. **Autenticación** — `POST /api/autenticacion/token`: credenciales
   GENÉRICAS (tabla + campoUsuario + campoContrasena + valores) →
   verifica BCrypt → emite JWT (Issuer/Audience/expiración del
   appsettings).
3. **Consultas** — `POST /api/consultas`: SELECT parametrizado (solo
   lectura) con parámetros nombrados.
4. **Procedimientos** — `POST /api/procedimientos/ejecutarsp`: ejecuta
   por nombre los SPs de la BD (los de factura y los de usuarios/roles
   que viajan en los scripts desde la v1) con sus parámetros.
5. **Estructuras** — exploración de tablas y columnas (el "descubrir en
   runtime" hecho endpoint).
6. **Diagnóstico** — `GET /api/diagnostico/conexion`: motor activo y
   estado de la conexión.

## 4. Requisitos no funcionales

- **RNF1 — `api_facturas` intacta:** `git diff v5` no toca nada del
  componente por-entidad.
- **RNF2 — Multi-motor real:** el componente corre contra postgres,
  sqlserver y mariadb con el MISMo interruptor del compose.
- **RNF3 — El secreto sigue sin viajar:** las lecturas de la genérica
  filtran los campos hasheados en la respuesta de verificación; el hash
  BCrypt vive en la BD.
- **RNF4 — Sin anticipación:** nada del front (v7).

## 5. Criterios de aceptación

1. **Regresión intacta:** la batería completa de la v5 (v1+v2+v3 por
   entidad) pasa tal cual contra el motor por defecto —
   `"version":"v6"` en el diagnóstico de api_facturas es el único cambio.
2. **El componente arriba:** `GET :8043/api/diagnostico/conexion`
   responde con el motor activo.
3. **El flujo JWT completo:** crear un usuario vía
   `POST /api/usuario?camposEncriptar=contrasena` (el hash queda BCrypt)
   → `POST /api/autenticacion/token` → 200 con token · con contraseña
   mala → 401 · `GET /api/producto` SIN token → 401 · CON token → 200
   con las filas como diccionarios.
4. **Las 12 tablas operables:** con token, `GET /api/rol`,
   `GET /api/ruta` y `GET /api/rol_usuario` responden (las tablas que la
   API por-entidad nunca cubrió).
5. **Consultas y SPs:** `/api/consultas` ejecuta un SELECT parametrizado
   · `/api/procedimientos/ejecutarsp` ejecuta
   `sp_consultar_factura_y_productosporfactura` y devuelve el JSON del
   SP.
6. **Multi-motor:** con `MOTOR_BD=sqlserver` (y `mariadb`), el
   diagnóstico del componente refleja el motor y el CRUD genérico
   responde igual.

## 6. Definición de TERMINADA

Los 6 criterios pasan → commit + tag `v6` → el sistema tiene sus dos
APIs contra tres motores → recién entonces se especifica la v7 (el front
Flask + Jinja2 que las consume).

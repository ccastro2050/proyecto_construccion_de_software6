# Plan — Versión 6: la API genérica de plataforma

> Cómo se integra lo especificado en [2_spec.md](2_spec.md). A diferencia
> de las versiones anteriores, la v6 no se construye rebanada por
> rebanada: el componente `api_generica_csharp/` es **infraestructura de
> referencia PROVISTA por el curso** (como `db/` desde la v1) — se
> integra, se estudia y se consume. Su construcción interna tiene su
> propio spec kit en `api_generica_csharp/docs/spec_kit/`.

---

## 1. Inventario de la versión

**Nuevo (1 componente + su carpeta):**

```
api_generica_csharp/               ← el componente completo (~10.000 líneas)
├── Controllers/                     Autenticacion · Consultas · Diagnostico
│                                    · Entidades · Estructuras · Procedimientos
├── Servicios/                       ServicioCrud · ServicioConsultas ·
│                                    ProveedorConexion · PoliticaTablasProhibidas
│                                    · EncriptacionBCrypt
├── Repositorios/                    Lectura y Consultas × 3 motores
├── Modelos/ConfiguracionJwt.cs
├── GUIA_USO_ENTIDADES.md            el manual de uso del CRUD genérico
├── GUIA_USO_PROCEDIMIENTOS.md       el manual de ejecutarsp
├── ApiGenericaCsharp.http           peticiones listas para VS Code/Rider
└── docs/spec_kit/                   el spec kit INTERNO del componente
```

**Crecen:**

| Archivo | Qué crece |
|---|---|
| `docker-compose.yml` | ★ servicio `api-generica-csharp` (:8043) con las 3 cadenas y `DatabaseProvider: ${MOTOR_BD:-postgres}` — el MISMO interruptor para las dos APIs |
| `api_facturas/Program.cs` | ★ solo el diagnóstico: `"version": "v6"` |

**Intocables:** TODO el resto de `api_facturas` (RNF1) y `db/`.

## 2. La arquitectura del componente (para leerlo, no para copiarlo)

Las MISMAS capas del curso, con un giro genérico:

- **Controllers** delgados que traducen HTTP ↔ servicio (igual que
  siempre) — pero `{tabla}` es un parámetro de ruta, no un nombre de
  clase.
- **ServicioCrud** valida nombres (tabla/columnas contra el catálogo del
  motor — ESA es la defensa contra inyección cuando el SQL se arma en
  runtime), aplica la política de tablas prohibidas y el BCrypt de
  `camposEncriptar`.
- **Repositorios por motor** (lectura y consultas × postgres, sqlserver,
  mariadb) elegidos por `DatabaseProvider` — la fábrica del curso, en
  versión "registro por switch" (compare con `Fabricas/` de
  api_facturas: mismo problema, otra forma).
- **Dapper** como ejecutor micro-ORM: aquí las filas SON diccionarios
  (no hay clases entidad que mapear) — no contradice la constitución de
  api_facturas: es OTRO componente con OTRO contrato, y el SQL sigue
  visible.

## 3. Seguridad (el modelo del componente)

- **JWT**: `POST /api/autenticacion/token` verifica las credenciales
  contra CUALQUIER tabla (BCrypt) y emite el token con la clave/emisor/
  audiencia de `appsettings.json`. `GET /api/{tabla}` exige el token
  (`[Authorize]`); el resto de verbos quedan abiertos en desarrollo (el
  endurecimiento por rol llega con el front y RBAC).
- **BCrypt por campo**: `?camposEncriptar=contrasena` — el hash se
  aplica al ESCRIBIR; `verificar-contrasena` compara sin exponer.
- **Tablas prohibidas**: lista en configuración que corta con 403 antes
  de tocar la BD.

## 4. Integración al compose

- Puerto **8043** (curso; estudiante 8143). Swagger en `/swagger`.
- Las tres cadenas viajan por variables `ConnectionStrings__X`; el
  interruptor es el MISMO `MOTOR_BD` de api_facturas: un solo `$env:`
  cambia el motor de TODO el sistema.
- `depends_on`: los tres motores listos (postgres healthy,
  sqlserver-init completado, mariadb healthy).

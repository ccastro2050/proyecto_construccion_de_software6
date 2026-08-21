# Quickstart — Versión 6: las dos APIs contra tres motores

> **Versión 6** · Validación rápida de la versión ya integrada.

---

## 1. Arrancar TODO

```powershell
docker compose up -d --build
```

Seis servicios: los tres motores (+ `sqlserver-init` Exited 0),
`api-facturas` (:8042) y **`api-generica-csharp` (:8043)** — su primera
compilación también toma ~1 minuto.

## 2. Regresión: api_facturas intacta (criterio 1)

Correr la batería de la [v5](../v5_mariadb/7_quickstart.md) §2 contra el
motor por defecto. Única diferencia: `"version":"v6"`.

## 3. Smoke test del componente (criterios 2 a 5)

```powershell
# 2. El componente respira (y dice su motor)
curl.exe http://localhost:8043/api/diagnostico/conexion

# 3. EL FLUJO JWT COMPLETO
# 3a. Crear un usuario con la contraseña HASHEADA por la API:
curl.exe -X POST "http://localhost:8043/api/usuario?camposEncriptar=contrasena" -H "Content-Type: application/json" -d "{\"email\":\"qa6@test.com\",\"contrasena\":\"secreto6\"}"
# 3b. Login → token:
curl.exe -X POST http://localhost:8043/api/autenticacion/token -H "Content-Type: application/json" -d "{\"tabla\":\"usuario\",\"campoUsuario\":\"email\",\"campoContrasena\":\"contrasena\",\"usuario\":\"qa6@test.com\",\"contrasena\":\"secreto6\"}"
# ← copie el token de la respuesta. Con contraseña mala → 401.
# 3c. GET protegido: SIN token → 401; CON token → 200 (diccionarios):
curl.exe -i http://localhost:8043/api/producto
curl.exe http://localhost:8043/api/producto -H "Authorization: Bearer SU_TOKEN"

# 4. LAS 12 TABLAS (las que la API por-entidad nunca cubrió):
curl.exe "http://localhost:8043/api/rol?limite=10" -H "Authorization: Bearer SU_TOKEN"
curl.exe "http://localhost:8043/api/ruta?limite=20" -H "Authorization: Bearer SU_TOKEN"
curl.exe "http://localhost:8043/api/rol_usuario?limite=30" -H "Authorization: Bearer SU_TOKEN"

# 5. CONSULTAS y PROCEDIMIENTOS:
curl.exe -X POST http://localhost:8043/api/consultas -H "Content-Type: application/json" -d "{\"consulta\":\"SELECT codigo, nombre, stock FROM producto WHERE stock > @minimo ORDER BY codigo\",\"parametros\":{\"minimo\":20}}"
curl.exe -X POST http://localhost:8043/api/procedimientos/ejecutarsp -H "Content-Type: application/json" -d "{\"nombreSP\":\"sp_consultar_factura_y_productosporfactura\",\"p_numero\":1,\"p_resultado\":null}"

# limpieza:
curl.exe -X DELETE "http://localhost:8043/api/usuario/qa6@test.com?nombreClave=email" -H "Authorization: Bearer SU_TOKEN"
```

> Los formatos exactos de cada grupo (PUT/PATCH genéricos, esquemas,
> filtros): [GUIA_USO_ENTIDADES](../../../../api_generica_csharp/GUIA_USO_ENTIDADES.md)
> y [GUIA_USO_PROCEDIMIENTOS](../../../../api_generica_csharp/GUIA_USO_PROCEDIMIENTOS.md),
> o el Swagger en http://localhost:8043/swagger.

## 4. Multi-motor (criterio 6)

```powershell
$env:MOTOR_BD = "sqlserver"          # (o "mariadb")
docker compose up -d api-facturas api-generica-csharp
curl.exe http://localhost:8042/                          # motor: sqlserver
curl.exe http://localhost:8043/api/diagnostico/conexion  # el MISMO motor
# … y el CRUD genérico responde igual (repita 3b-3c).
Remove-Item Env:MOTOR_BD
docker compose up -d api-facturas api-generica-csharp
```

## 5. Si algo falla

| Síntoma | Causa probable |
|---|---|
| Los de v1-v5 | Aplican todos igual |
| :8043 no responde | Primera compilación en curso — `docker compose logs api-generica-csharp` |
| 401 en el login con el usuario recién creado | ¿Creó el usuario SIN `?camposEncriptar=contrasena`? El login compara BCrypt: texto plano nunca valida |
| 401 con token en mano | El header es `Authorization: Bearer TOKEN` (espacio incluido); el token expira en 60 min |
| 403 en una tabla | Está en `TablasProhibidas` del appsettings |
| ejecutarsp devuelve error de parámetros | Los nombres de parámetro deben calzar con el SP (`p_numero`, `p_resultado`…) — ver la GUIA_USO |

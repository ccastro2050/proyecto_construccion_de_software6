# Quickstart — Versión 6: arranque y smoke test del front

## 1. Arranque (un solo comando, ahora con 6 servicios)

```powershell
docker compose up -d --build
```

Servicios: postgres · sqlserver (+init) · mariadb · api-facturas (:8047) ·
**front-flask (:8049)**.

## 2. Regresión de la API (criterio 1)

El smoke de la [v5](../v5_mariadb/7_quickstart.md) pasa completo; el
diagnóstico dice `"version":"v6"`.

## 3. Smoke test del front (criterios 2 a 5)

```powershell
# 3a. Un usuario de prueba, creado POR LA API (el front no registra usuarios):
curl.exe -X POST http://localhost:8047/api/usuario -H "Content-Type: application/json" -d "{\"email\":\"demo@correo.com\",\"contrasena\":\"Demo123!\"}"

# 3b. EN EL NAVEGADOR — http://localhost:8049
#  · sin sesión, /productos redirige a /login                (criterio 2)
#  · login con demo@correo.com / Demo123!  → la tabla de productos
#  · login con clave mala                  → "credenciales incorrectas"
#  · Nuevo producto: PR050 / Probador / 5 / 1000 → aparece en la tabla (criterio 3)
#  · Editar PR050: SOLO stock=9 → la tabla muestra 9 (fue un PATCH)
#  · Eliminar PR050 → la tabla vuelve a 8
#  · Nuevo producto con stock -5 → el error del 422 JUNTO al campo   (criterio 4)

# 3c. La prueba de la frontera: el dato viajó por la API (no por magia):
curl.exe http://localhost:8047/api/producto            # los mismos 8 de la tabla
```

## 4. Si algo falla

| Síntoma | Causa probable |
|---|---|
| El front carga pero "el servicio no está disponible" | La API no está arriba aún (dotnet watch compila ~40 s) — espere y refresque |
| Login siempre "usuario no existe" | No creó el usuario del paso 3a (o la BD se reseteó con `down -v`) |
| /productos muestra login otra vez | La sesión expiró o `CLAVE_SESION` cambió entre reinicios |
| Estilos sin marca | Fuerce recarga (Ctrl+F5): el navegador cacheó el CSS |

# Contratos — Versión 6: las PANTALLAS del front (y los 51 de la API, intactos)

> El contrato de un front no son endpoints JSON: son **rutas que devuelven
> HTML** y formularios que envían POST. Base: `http://localhost:8049`.
> Los 51 contratos de la API siguen vigentes tal cual (solo el diagnóstico
> pasa a `"version":"v6"`).

## A. Autenticación

```
GET  /login      → 200 la página de login (marca completa; sin sesión requerida)
POST /login      body form: usuario, contrasena
                 → 302 a /productos (sesión iniciada) · 200 el mismo login con
                   mensaje "credenciales incorrectas" (401 de la API) o
                   "usuario no existe" (404 de la API)
GET  /logout     → 302 a /login (sesión destruida)
GET  /           → 302 a /productos (con sesión) · 302 a /login (sin sesión)
```

## B. Productos (toda ruta exige sesión; sin ella → 302 a /login)

```
GET  /productos                    → 200 tabla con los productos (GET /api/producto)
GET  /productos/nuevo              → 200 formulario vacío
POST /productos/nuevo              → 302 a /productos con mensaje de éxito ·
                                     200 el formulario con los errores del 422 por campo
GET  /productos/{codigo}/editar    → 200 formulario precargado · 302 con mensaje si 404
POST /productos/{codigo}/editar    → PATCH a la API con SOLO lo diligenciado →
                                     302 a /productos · 200 con errores
POST /productos/{codigo}/eliminar  → 302 a /productos con mensaje (200 o el 404 "ya no existe")
```

**Regla de traducción de errores de la API** (el front nunca muestra trazas):

| La API respondió | El front muestra |
|---|---|
| 422 con `errores[]` | El mismo formulario, cada error junto a su campo (Rojo Anulada) |
| 400 / 404 / 409 | El `mensaje` de la API como aviso con la marca |
| 500 / API caída | "El servicio no está disponible" + el `detalle` si existe |

## C. El diagnóstico de la API (única línea que cambia)

```
GET :8047/  → {"mensaje":"API Facturas funcionando","version":"v6","motor":"...","contratos":".../v6_front_producto/6_contracts.md"}
```

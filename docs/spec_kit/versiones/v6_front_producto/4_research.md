# Investigación y decisiones — Versión 6 (el front)

## D1 — ¿Sesión de Flask o JWT?
**Contexto:** el front necesita saber quién está logueado. La API ofrece
`verificar-contrasena` (200/401/404) pero no emite tokens.
**Opciones:** (a) implementar JWT en la API (tocarla) · (b) sesión de
servidor en Flask: cookie firmada tras el 200 de verificar-contrasena ·
(c) sin login en v6.
**Decisión: (b).** No toca la API (RNF2), es el mecanismo natural de un
front server-side, y enseña el segundo modelo de autenticación del curso
(la sesión) — JWT quedará para cuando haya clientes que no son navegador.
**Consecuencias:** la clave de firma viaja por variable de entorno; el
control por roles (v7) se hará leyendo rol_usuario/rutarol desde la API.

## D2 — ¿Por qué Flask + Jinja2 si el back es C#?
**Opciones:** (a) Razor/Blazor (mismo stack) · (b) Flask + Jinja2.
**Decisión: (b)** — decisión del curso desde el mapa: un front en OTRO
lenguaje demuestra que la única frontera real es el contrato HTTP; si el
front solo funcionara "porque comparte lenguaje", las capas serían mentira.

## D3 — ¿Por qué una marca inventada?
Un front sin identidad termina siendo Bootstrap por defecto y cada
estudiante decora a su gusto. El [Manual de Marca](../../../MANUAL_DE_MARCA.md)
convierte el diseño visual en ESPECIFICACIÓN verificable (criterio 5):
paleta con nombres, tipografías y usos prohibidos — como en la industria.

## D4 — ¿Por qué solo producto en la v6?
La misma razón de la v1: una rebanada completa vale más que doce a
medias. v7 replica el molde a las 12 entidades (con roles); v8 monta la
facturación — el front también respeta "no se anticipa".

## D5 — Server-side rendering puro (sin JavaScript de framework)
El curso enseña la mecánica HTTP (formularios, redirecciones, códigos);
un framework JS la esconde. El fetch/JS llegará donde aporte (v8, si los
renglones de factura lo exigen — se decidirá allá).

# Research — Versión 6: decisiones y alternativas

> Lectura opcional: el PORQUÉ de cada decisión del [plan](3_plan.md).

---

## D1 — ¿Componente provisto, o construido rebanada a rebanada?

Las v1-v5 se construyen; la v6 se **integra**. **Por qué:** el componente
mide ~10.000 líneas con problemas que no son los objetivos del curso
(catálogos de metadatos por motor, políticas de seguridad, JWT completo).
Construirlo desde cero tomaría el semestre entero. La decisión es la
misma que con la BD en la v1: infraestructura DADA, con su documentación
(las GUIA_USO y su spec kit interno) — y el estudiante la ESTUDIA con el
mapa del plan §2 y la reconstruye por partes en la GUIA_IA6.

## D2 — ¿Por qué convive con api_facturas en vez de reemplazarla?

Porque el CONTRASTE es la lección: la por-entidad valida con tipos en la
frontera (422 con errores[]) y da contratos exactos; la genérica cubre
las 12 tablas sin una rebanada por tabla, pero valida contra el catálogo
en runtime y sus filas son diccionarios. Ninguna reemplaza a la otra en
la industria — se eligen por caso. Tenerlas lado a lado contra los
MISMOS motores hace la comparación tangible.

## D3 — Dapper en la genérica (y no en api_facturas)

La constitución de api_facturas prohíbe ORM para que el SQL quede
visible y el mapeo fila→objeto se entienda. En la genérica NO HAY clases
entidad (las filas son diccionarios por diseño), así que un micro-ORM
como Dapper es solo un ejecutor cómodo — el SQL sigue escrito a mano. La
regla no se rompe: cada componente tiene su constitución.

## D4 — Un solo interruptor (MOTOR_BD) para las dos APIs

El compose pasa `MOTOR_BD` a api_facturas (clave `Motor`) y a la
genérica (clave `DatabaseProvider`). Alternativa: interruptores
separados por API. **Decisión: uno solo** — el escenario didáctico
típico es "todo el sistema contra el motor X", y un solo `$env:` lo
logra. (Quien quiera mezclarlos puede editar el compose: las variables
son independientes por servicio.)

## D5 — La seguridad de la genérica primero (y api_facturas abierta)

El JWT nace en la genérica porque su superficie lo exige (CUALQUIER
tabla). api_facturas queda abierta en la v6: protegerla con el mismo
token es un ejercicio natural del front (v7), cuando haya login de
verdad. Endurecer todo hoy solo estorbaría la regresión.

## D6 — Puerto 8048

La familia del curso: 8047 (facturas) → **8048 (genérica)**. Estudiante:
8148. El front (v7) tomará 8044.

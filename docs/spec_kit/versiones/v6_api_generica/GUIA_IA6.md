# Cómo abordar la VERSIÓN 6 con IA — sobre su proyecto de la v5

> La v6 es DISTINTA: el componente `api_generica_csharp` es referencia
> PROVISTA (como la BD desde la v1) — no se le pide a la IA que escriba
> 10.000 líneas. El trabajo de esta versión es INTEGRAR, ESTUDIAR y
> RECONSTRUIR UNA rebanada representativa.

---

## 0. Punto de partida

Su proyecto con la **v5 funcionando** (regresión triple en verde, sus
puertos +100). Sus puertos nuevos: **API genérica 8143**.

## Parte A — Integrar (sin IA: son copias y configuración)

1. Copie `api_generica_csharp/` completo del clon del curso.
2. Adapte `appsettings.json` (sus puertos +100, SU clave JWT de mínimo
   32 caracteres) y el `Dockerfile` (8143).
3. Agregue el servicio al `docker-compose.yml`
   ([plan §4](3_plan.md)) con `DatabaseProvider: ${MOTOR_BD:-postgres}`.
4. Corra el [quickstart](7_quickstart.md) completo (§2 a §4). Hasta aquí
   no escribió código — pero ya tiene el sistema de dos APIs.

## Parte B — Estudiar (el ejercicio evaluable)

Recorra el componente con el mapa del [plan §2](3_plan.md) y responda
por escrito (para la sustentación):

1. ¿Dónde valida el componente que `{tabla}` existe ANTES de armar SQL,
   y por qué eso detiene la inyección de identificadores?
2. ¿Qué viaje hace la contraseña en `?camposEncriptar=` y en el login?
   ¿En qué se parece al RepositorioUsuario de su v3?
3. Compare el `switch` de `Program.cs` (registro por DatabaseProvider)
   con SU `Fabricas/`: ¿qué patrón es, qué cambia entre las dos formas?

## Parte C — Reconstruir UNA rebanada con IA (el reto)

Pídale a la IA que reescriba, EN UN PROYECTO APARTE de práctica, el
`AutenticacionController` + la verificación BCrypt (el flujo token
completo) usando como contrato la
[GUIA_USO_ENTIDADES](../../../../api_generica_csharp/GUIA_USO_ENTIDADES.md)
§verificar-contrasena y el [contrato](6_contracts.md) del token. Regla
de alcance para el prompt: *"solo el flujo de autenticación: credenciales
genéricas → verificación BCrypt contra la tabla indicada → JWT firmado
con la configuración; nada de CRUD"*. Compare su resultado con el del
curso — las diferencias son la conversación de la sustentación.

## La alarma de siempre

Si la IA le propone "mejorar" su `api_facturas` mientras integra
(unificar las dos APIs, meterle JWT, borrar rebanadas "redundantes"):
recháselo — el criterio 1 exige la regresión v5 intacta, y la
convivencia de las DOS filosofías es la lección de la versión.

## Cierre

Los 6 criterios del [2_spec.md](2_spec.md) en verde (con sus puertos
+100) → tag `v6`.

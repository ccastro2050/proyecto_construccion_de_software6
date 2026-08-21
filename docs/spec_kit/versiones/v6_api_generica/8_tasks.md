# Tareas — Versión 6: orden de integración por fases verificables

> La v6 se INTEGRA (el componente es referencia provista — [plan](3_plan.md)).

---

## Fase 0 — Punto de partida

- [ ] La v5 corre y su regresión triple pasa (tag `v5` presente).

## Fase 1 — El componente en el repositorio

- [ ] Copiar `api_generica_csharp/` del repo del curso (completo, con
      sus GUIA_USO y su spec kit interno).
- [ ] Adaptar `appsettings.json`: cadenas de SUS puertos, su clave JWT
      (mínimo 32 caracteres), `DatabaseProvider: Postgres`.
- [ ] `Dockerfile`: puerto 8043 (estudiante: 8143).

**Verificar:** `dotnet build` del componente compila.

## Fase 2 — La integración al compose

- [ ] Servicio `api-generica-csharp`: build, volúmenes (código + bin/obj
      anónimos), puerto, las 3 `ConnectionStrings__X` internas y
      `DatabaseProvider: ${MOTOR_BD:-postgres}`.
- [ ] `depends_on` de los tres motores.
- [ ] `api_facturas/Program.cs`: diagnóstico a `"version":"v6"` (único
      cambio del componente viejo).

**Verificar:** `docker compose up -d --build` → :8042 y :8043 responden.

## Fase 3 — El recorrido de seguridad

- [ ] El flujo JWT del [7_quickstart.md](7_quickstart.md) §3 (crear
      usuario hasheado → token → 401 sin token → 200 con token).
- [ ] Consultas y ejecutarsp (§3.5).

## Fase 4 — Multi-motor y cierre

- [ ] El interruptor con las DOS APIs ([quickstart §4](7_quickstart.md)).
- [ ] Regresión v5 intacta · README y mapa · commit + tag `v6` + push.

**Verificar:** los 6 criterios de [2_spec.md](2_spec.md) §5 en verde.

# Guía para construir la v6 con IA (el front)

> Reconstruya el front en SU carpeta (fuera del clon), con la API del
> curso corriendo. Puerto del estudiante: **8149**.

## El prompt (chat web o IDE agéntico)

Entregue a la IA: esta carpeta `v6_front_producto/` completa + el
[MANUAL_DE_MARCA.md](../../../MANUAL_DE_MARCA.md) + la
[constitución](../../1_constitution.md), y este encargo:

```
Construye EXACTAMENTE la versión 6 especificada en 2_spec.md: un front
Flask + Jinja2 (Python) llamado front_flask, puerto 8149, que consume la
API de facturas en http://localhost:8047 (variable de entorno
API_FACTURAS_URL). Sesión de Flask para el login sobre
POST /api/usuario/verificar-contrasena (D1 de 4_research.md). Solo la
entidad producto (nada de v7/v8). La marca del MANUAL_DE_MARCA.md como
variables CSS. El front NO toca la base de datos: su única fuente es la
API. Sigue las fases de 8_tasks.md en orden y no avances con una fase en
rojo. Español colombiano, trato de usted, sin ORM ni JavaScript de
framework.
```

## Las reglas de supervisión

1. **Fase por fase** (8_tasks): exija el "Verificar" antes de continuar.
2. Si la IA valida negocio en el front (stock < 0 en Python), deténgala:
   eso es de la API — el front solo muestra los errores que ella responda.
3. Si aparece una cadena de conexión en el front, deténgala: violó RNF1.
4. Cierre con el [quickstart](7_quickstart.md) completo — usted, no la IA.

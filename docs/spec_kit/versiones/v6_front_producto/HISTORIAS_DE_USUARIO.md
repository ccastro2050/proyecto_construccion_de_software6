# Historias de usuario — Versión 6: el front nace

> Proyecto Construcción de Software · USB Medellín. El formato de tarjetas
> del curso; trazabilidad de ida y vuelta con [2_spec.md](2_spec.md) y
> [6_contracts.md](6_contracts.md). Personas: **Marcela Ríos** (auxiliar de
> inventario) y **Álvaro Mejía** (administrador).

## Historial de revisiones

| Fecha | Versión | Descripción | Autor | Revisor |
|---|---|---|---|---|
| 27/08/2026 | 1.0 | Historias de la v6 (front: marca, login y producto) | Carlos Arturo Castro Castro | — |

---

## Historia de Usuario 1

| | | |
|---|---|---|
| **Número:** 1 | **Usuario:** Marcela Ríos — auxiliar de inventario | **Iteración asignada:** v6 |
| **Nombre historia:** Entrar al sistema con mi usuario | | |
| **Diseñada por:** Carlos Arturo Castro Castro | | |
| **Prioridad:** Alta | **Riesgo en desarrollo:** Medio | |
| **Puntos estimados:** 2 | **Horas estimadas:** 8 | |
| **Programador responsable:** el estudiante (ver [GUIA_IA6](GUIA_IA6.md)) | | |

**Descripción:**
Yo, Marcela Ríos, como auxiliar de inventario, quiero entrar al sistema
con mi correo y mi contraseña desde una página con la imagen de la
empresa, para trabajar el catálogo sin herramientas técnicas (ni Swagger
ni curl).

**Observaciones:**
Trazabilidad: RF1 de [2_spec.md](2_spec.md) · §A de
[6_contracts.md](6_contracts.md) · el login usa `verificar-contrasena`
de la API (v3) — nada se reimplementa.

**Criterios de aceptación:**
1. `/login` muestra la página con el logosímbolo del
   [manual de marca](../../../MANUAL_DE_MARCA.md).
2. Con credenciales válidas entro y veo los productos; con clave mala veo
   "credenciales incorrectas"; con usuario inexistente, "usuario no existe".
3. Sin sesión, cualquier página me devuelve al login; "salir" cierra la
   sesión de verdad (volver atrás no me deja adentro).

---

## Historia de Usuario 2

| | | |
|---|---|---|
| **Número:** 2 | **Usuario:** Marcela Ríos — auxiliar de inventario | **Iteración asignada:** v6 |
| **Nombre historia:** Ver y gestionar el catálogo desde el navegador | | |
| **Diseñada por:** Carlos Arturo Castro Castro | | |
| **Prioridad:** Alta | **Riesgo en desarrollo:** Medio | |
| **Puntos estimados:** 3 | **Horas estimadas:** 12 | |
| **Programador responsable:** el estudiante (ver [GUIA_IA6](GUIA_IA6.md)) | | |

**Descripción:**
Yo, Marcela Ríos, como auxiliar de inventario, quiero ver el catálogo en
una tabla y crear, corregir o retirar productos con formularios, para
hacer mi trabajo diario sin saber qué es un JSON.

**Observaciones:**
Trazabilidad: RF2–RF5 de [2_spec.md](2_spec.md) · §B de
[6_contracts.md](6_contracts.md). El front NO valida negocio: muestra lo
que la API responda (la pareja editar-parcial = PATCH visible).

**Criterios de aceptación:**
1. `/productos` muestra los 8 productos semilla con la tabla de la marca.
2. Creo PR050 con el formulario y aparece en la tabla; lo edito cambiando
   SOLO el stock y el cambio se ve; lo elimino y la tabla vuelve a 8.
3. Si envío datos malos, los errores de la API aparecen junto a cada
   campo — jamás una pantalla técnica de error.

---

## Historia de Usuario 3

| | | |
|---|---|---|
| **Número:** 3 | **Usuario:** Álvaro Mejía — administrador | **Iteración asignada:** v6 |
| **Nombre historia:** Que el sistema tenga la imagen de la empresa | | |
| **Diseñada por:** Carlos Arturo Castro Castro | | |
| **Prioridad:** Media | **Riesgo en desarrollo:** Bajo | |
| **Puntos estimados:** 1 | **Horas estimadas:** 6 | |
| **Programador responsable:** el estudiante (ver [GUIA_IA6](GUIA_IA6.md)) | | |

**Descripción:**
Yo, Álvaro Mejía, como administrador de Comercial Los Andes, quiero que
todas las pantallas usen la identidad de la empresa (colores, tipografía
y logosímbolo del manual), para que el sistema se vea NUESTRO y no como
una plantilla genérica de internet.

**Observaciones:**
Trazabilidad: RF6 de [2_spec.md](2_spec.md) · el
[MANUAL_DE_MARCA.md](../../../MANUAL_DE_MARCA.md) es la especificación
visual; `marca.css` su implementación.

**Criterios de aceptación:**
1. Header Azul Cordillera con el logosímbolo en negativo y el ▲ Ámbar.
2. Botones y estados usan la paleta con sus papeles (primario/éxito/
   peligro) — ningún color por fuera del manual.
3. Los mensajes de éxito y error llevan texto además del color.

## Referencias

1. Formato de tarjeta: *Historias de usuario — micro proyecto gestión del
   desempeño v2.5* (USB Medellín), adaptado al proyecto facturas.
2. En este kit: [2_spec.md](2_spec.md) · [6_contracts.md](6_contracts.md) ·
   [7_quickstart.md](7_quickstart.md) (los criterios, ejecutables).

# Riesgo de Selección Adversa en el Mercado Automotor Argentino
## Informe Ejecutivo — Entidades Financieras y Administradoras de Cartera

**Autor:** Rodolfo Gabriel Riveros Lobos  
**Fecha:** Junio 2026  
**Fuente de datos:** DNRPA — Dirección Nacional de los Registros de la Propiedad Automotor  
**Período analizado:** Enero 2023 — Mayo 2026 (41 meses)

---

## Resumen ejecutivo

El mercado de autos usados en Argentina presenta un mecanismo de transmisión
de riesgo medible y anticipable: cuando el volumen de patentamientos 0km cae,
la calidad promedio del mercado secundario se deteriora aproximadamente
**60 días después**.

Este desfase temporal fue confirmado mediante análisis econométrico formal
(Test de Causalidad de Granger, p<0.05 en lags 1 a 4) sobre 41 meses de
datos transaccionales de la DNRPA.

Para una entidad financiera con cartera de créditos automotores sobre usados,
este mecanismo representa un **riesgo de garantía no gestionado**: el activo
que respalda el crédito puede depreciarse más rápido de lo que el modelo de
scoring tradicional anticipa, precisamente en los momentos de mayor estrés
macroeconómico.

---

## El mecanismo de riesgo

### ¿Qué es la selección adversa en el mercado automotor?

Akerlof (1970) demostró que cuando el comprador no puede verificar la calidad
de un bien antes de adquirirlo, el mercado tiende a llenarse de unidades de
baja calidad — los llamados "limones". Los vendedores de unidades buenas
("duraznos") no participan porque el precio de mercado no refleja su calidad real.

En el mercado automotor argentino, esta dinámica opera de la siguiente manera:

```
Shock en 0km (sobrestock, devaluación, apertura de importaciones)
        ↓
Compradores solventes migran al mercado primario
        ↓  [~60 días]
Mercado de usados pierde compradores de calidad
        ↓
Proporción de "limones" aumenta en el mercado secundario
        ↓
Riesgo de garantía sube para créditos sobre usados
```

### El ISA como termómetro de riesgo

El **Índice de Selección Adversa (ISA)** cuantifica mensualmente el nivel de
deterioro del mercado de usados, construido a partir de dos variables de la DNRPA:

- **Antigüedad media** de los vehículos transaccionados (proxy directo de calidad)
- **Participación de vehículos Protocolo 21** (Mercosur) — mayor participación
  indica parque más joven, menor deterioro

Un ISA positivo indica mercado con exceso de "limones".
Un ISA negativo indica mercado con predominio de "duraznos".

---

## Hallazgos del análisis

### Comportamiento del ISA en el período analizado

| Evento | Período | ISA | Interpretación |
|---|---|---|---|
| Línea de base | 2023 (promedio) | ≈ 0.00 | Mercado en equilibrio estructural |
| Pico de estrés | Enero 2024 | +2.84 | Máximo deterioro post-devaluación |
| Recuperación | Mayo–Agosto 2024 | Negativo | Normalización gradual |
| Nuevo deterioro | Diciembre 2025 | -2.44 | Anomalía estacional + apertura importaciones |

### Precedencia temporal confirmada

El volumen de patentamientos 0km **anticipa** el ISA con un desfase de 1 a 4 meses.
La correlación máxima se registra a los 2 meses (r = -0.452, significativa al 95%).

Esto significa: **cuando los patentamientos 0km caen hoy, el mercado de usados
se deteriora en 60 días**. El ISA puede funcionar como sistema de alerta temprana.

### Relación estructural de largo plazo

Las series de volumen 0km e ISA están **cointegradas** (Test de Engle-Granger,
p = 0.0025): aunque en el corto plazo pueden divergir, comparten un equilibrio
estructural del que no se alejan indefinidamente. Esto confirma que la relación
entre ambos mercados no es circunstancial sino sistémica.

---

## Implicancias para la gestión de cartera

### Riesgo de garantía dinámico

Los modelos de scoring automotor tradicionales utilizan el valor del vehículo
al momento del otorgamiento del crédito. El ISA introduce una dimensión dinámica:
el valor de la garantía no es estático — fluctúa con la calidad del mercado.

Un crédito otorgado en un contexto de ISA bajo (mercado de calidad) tiene menor
riesgo de garantía que el mismo crédito otorgado con ISA alto, aun con el mismo
vehículo y el mismo deudor.

### Aplicaciones concretas

**Pricing dinámico de riesgo**
Incorporar el ISA como variable en el modelo de tasa de interés para créditos
sobre usados. Períodos de ISA alto → spread adicional que compense el mayor
riesgo de depreciación de garantía.

**Alertas de deterioro de cartera**
Monitoreo mensual del ISA para anticipar ventanas de estrés. Una caída
sostenida del volumen 0km activa una alerta 60 días antes de que el deterioro
se materialice en el mercado secundario.

**Segmentación por antigüedad**
El componente de antigüedad del ISA permite identificar los segmentos de cartera
más expuestos: créditos sobre vehículos de mayor antigüedad media son más
sensibles a los shocks de selección adversa.

---

## Limitaciones del modelo

La credibilidad de este análisis requiere declarar sus límites:

**Ausencia de precios**
El ISA es un índice volumétrico y composicional. No cuantifica la depreciación
en pesos por unidad. La magnitud del impacto sobre el valor de garantía requiere
integración con datos de precios (InfoAuto, Kavak, subastas).

**Variables macroeconómicas omitidas**
Tipo de cambio, inflación (IPC) y tasas de interés (Badlar) afectan
simultáneamente a ambos mercados. El efecto cascada documentado puede estar
parcialmente contaminado por shocks macroeconómicos comunes. Se recomienda
incorporar estos controles en una versión extendida del modelo.

**Sensibilidad del índice**
El resultado de precedencia temporal es estadísticamente significativo con la
especificación base del ISA (p=0.041) pero marginal con especificaciones
alternativas (p=0.052 y p=0.104). La señal existe pero requiere validación
con datos adicionales.

**Punto ciego de Akerlof**
La DNRPA registra transacciones completadas. Las transacciones frustradas —
compradores que abandonaron el mercado por no encontrar calidad suficiente —
son invisibles para el modelo.

---

## Próximos pasos recomendados

| Acción | Descripción | Impacto |
|---|---|---|
| Integración con precios | Cruzar ISA con datos de InfoAuto o subastas | Cuantificar depreciación en pesos |
| Controles macro | Incorporar IPC, tipo de cambio y Badlar al modelo | Aislar efecto cascada puro |
| Dashboard de monitoreo | ISA mensual automatizado en Power BI / Looker Studio | Alertas tempranas para equipos de riesgo |
| Extensión a segmentos | Calcular ISA por segmento de antigüedad y marca | Granularidad para pricing diferenciado |

---

## Datos y reproducibilidad

El análisis completo, el código fuente y la metodología están disponibles en:

**[github.com/RGRIVEROS-PORTFOLIO/mercado-limones-causal](https://github.com/RGRIVEROS-PORTFOLIO/mercado-limones-causal)**

Fuente de datos: DNRPA — datos.gob.ar (acceso público)

---

*Este informe fue producido con estándares de ciencia de datos reproducible
(Wilson et al., 2017). Todos los resultados son verificables y replicables
a partir del repositorio público.*

**Rodolfo Gabriel Riveros Lobos**
Analista de Datos — San Juan, Argentina
[![GitHub](https://img.shields.io/badge/GitHub-RGRIVEROS--PORTFOLIO-black)](https://github.com/RGRIVEROS-PORTFOLIO)
[[Linkedin/RGRIVEROS](https://www.linkedin.com/in/rgriveros/)]
Mail: rgriveros@gmail.com
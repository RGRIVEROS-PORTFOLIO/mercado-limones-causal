# El Reloj del Mercado de Usados
## Informe para Concesionarios y Operadores del Mercado Automotor Argentino

**Autor:** Rodolfo Gabriel Riveros Lobos  
**Fecha:** Junio 2026  
**Fuente de datos:** DNRPA — Dirección Nacional de los Registros de la Propiedad Automotor  
**Período analizado:** Enero 2023 — Mayo 2026 (41 meses)

---

## La pregunta de negocio

¿Existe una forma de anticipar cuándo el mercado de usados va a deteriorarse,
antes de que ese deterioro afecte el valor de tu stock?

La respuesta que encontramos es sí — y el indicador adelantado está en los
datos de patentamientos 0km de la DNRPA.

---

## El mecanismo que descubrimos

Cuando el mercado de 0km sufre una caída en los patentamientos —
ya sea por sobrestock, devaluación o apertura de importaciones —
**el mercado de usados se deteriora aproximadamente 60 días después**.

¿Por qué? El comprador solvente, el que puede elegir entre 0km y usado,
migra al mercado primario cuando aparecen oportunidades (descuentos,
financiación agresiva, nuevos modelos importados). El mercado de usados
pierde a sus mejores compradores y queda con mayor proporción de
vendedores de unidades de baja calidad que no encuentran precio.

Este desfase de 60 días es medible, reproducible y estadísticamente
confirmado sobre 41 meses de datos reales de la DNRPA.

---

## Lo que pasó en Argentina 2023-2026

### El shock de enero 2024

La devaluación de diciembre 2023 colapsó los patentamientos 0km en el
último trimestre de 2023. Exactamente 60 días después, en enero-febrero
2024, el mercado de usados registró su peor nivel de calidad del período
analizado — el Índice de Selección Adversa (ISA) alcanzó su pico máximo.

Los concesionarios que no anticiparon este deterioro enfrentaron:
- Stock de usados valuado sobre un mercado que ya no sostenía esos precios
- Mayor dificultad para colocar unidades de antigüedad media-alta
- Compradores más cautelosos y negociadores en precio

### La recuperación de 2024

Entre mayo y agosto 2024, el ISA volvió a territorio negativo — el mercado
de usados mejoró su calidad promedio. Esto coincidió con la estabilización
del tipo de cambio y la recuperación gradual de los patentamientos 0km.

### El nuevo contexto 2025-2026

La apertura de importaciones incorporó vehículos más jóvenes al mercado,
modificando la composición del parque circulante. El ISA refleja este cambio
estructural: el mercado de usados tiene hoy una dinámica diferente a la
del período pre-apertura.

---

## Cómo usar esta información en tu operación

### Timing de compra de stock

El ISA funciona como termómetro del mercado. Cuando el ISA está en zona
positiva (mercado deteriorado) y los patentamientos 0km muestran señales
de recuperación, tenés una ventana de aproximadamente 60 días antes de
que la calidad del mercado de usados mejore.

Ese es el momento de **comprar stock selecto a precios de mercado deteriorado**
antes de que la mejora se refleje en los precios de referencia.

### Timing de liquidación

A la inversa: cuando los patentamientos 0km caen sostenidamente durante
dos o tres meses, el deterioro del mercado de usados está por llegar.
Ese es el momento de **rotar stock de antigüedad media-alta** antes de
que la presión compradora se debilite.

### Segmentación por antigüedad

El deterioro no afecta a todos los segmentos por igual. Las unidades
de mayor antigüedad son las más sensibles a los shocks de selección adversa —
son las primeras en perder valor cuando el mercado se deteriora y las
últimas en recuperarse.

Las unidades jóvenes (hasta 3 años) mantienen mejor su valor incluso
en contextos de ISA alto, porque el comprador que las busca tiene menos
alternativas en el mercado primario.

---

## El dato concreto

| Situación | Señal de alerta | Tiempo de anticipación |
|---|---|---|
| Caída de patentamientos 0km | ISA sube en ~60 días | 2 meses |
| Recuperación de patentamientos 0km | ISA baja en ~60 días | 2 meses |
| ISA > +1.5 | Mercado deteriorado — precaución en compra de stock antiguo | — |
| ISA < -1.5 | Mercado de calidad — oportunidad de posicionamiento | — |

---

## Limitaciones importantes

Este análisis trabaja con volúmenes y composición del parque, no con precios.
El ISA indica **cuándo** el mercado se deteriora, no **cuánto** bajan los precios.
Para cuantificar el impacto en pesos, es necesario cruzar con datos de
InfoAuto o precios de subasta.

El modelo fue desarrollado sobre el período 2023-2026 e incluye el shock
extraordinario de la devaluación Milei. Su capacidad predictiva en contextos
de estabilidad macroeconómica sostenida está por validarse con datos futuros.

---

## Acceso al análisis completo

La metodología, el código y los datos históricos están disponibles en:

**[github.com/RGRIVEROS-PORTFOLIO/mercado-limones-causal](https://github.com/RGRIVEROS-PORTFOLIO/mercado-limones-causal)**

Para consultas sobre aplicaciones específicas a tu operación:

**Rodolfo Gabriel Riveros Lobos**
Analista de Datos — San Juan, Argentina
[![GitHub](https://img.shields.io/badge/GitHub-RGRIVEROS--PORTFOLIO-black)](https://github.com/RGRIVEROS-PORTFOLIO)
[[Linkedin/RGRIVEROS](https://www.linkedin.com/in/rgriveros/)]
Mail: rgriveros@gmail.com
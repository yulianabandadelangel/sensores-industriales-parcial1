# Informe — Primer parcial Manejo Masivo de Datos

**Autor:** Yuliana Elizabeth Banda Del Angel
**Profesor:** Javier Moya
**Fecha:** 5 de octubre de 2026

Este informe aplica los conceptos de Big Data al análisis de los sensores
industriales realizado en `analisis.py`. Los datos del CSV son **simulados**.

---

## 5. Las 5 V aplicadas al proyecto

| V | ¿Cómo se relaciona? | Ejemplo concreto | ¿En el CSV actual o ampliación? |
|---|---------------------|------------------|---------------------------------|
| **Volumen** | Cantidad de mediciones acumuladas por los sensores a lo largo del tiempo. | El CSV actual tiene 100,000 lecturas; al escalar a miles de sensores con lecturas por segundo se pasaría a miles de millones de registros al día. | CSV actual (100,000 filas) y ampliación (futura escala masiva). |
| **Velocidad** | Rapidez con la que llegan y se procesan nuevas lecturas. | Hoy el CSV se analiza por lotes (todo el archivo ya guardado). En la ampliación, cada sensor enviará una medición por segundo que debe procesarse casi en tiempo real. | Ampliación futura. |
| **Variedad** | Diferentes formatos y tipos de datos que la empresa planea manejar. | Hoy solo hay datos tabulares (CSV con número, fecha y texto). En el futuro se integrarán fotografías de las máquinas (imágenes) y reportes de mantenimiento (texto libre). | CSV actual (estructurado) y ampliación (semi/no estructurados). |
| **Veracidad** | Confianza y calidad de los datos recibidos. | Los datos son simulados, pero podrían tener lecturas erróneas, sensores descalibrados o valores atípicos (ej. 104.99 °C). Hay que validar el dato antes de usarlo para decidir. | CSV actual (lecturas máximas sospechosas) y ampliación (fallas de sensores reales). |
| **Valor** | Qué información útil se extrae para la empresa. | Detectar que la **Planta_3** concentra 1,777 alertas permite priorizar mantenimiento preventivo ahí. | CSV actual (hallazgos accionables del análisis). |

---

## 6. Tipos de datos y procesamiento tradicional

### Clasificación de cada elemento

| Elemento | Tipo | Justificación |
|----------|------|---------------|
| El CSV de sensores | **Estructurado** | Tiene columnas definidas con tipos conocidos (fecha, texto, número) y filas uniformes; se puede consultar con SQL o pandas. |
| Un mensaje JSON enviado por un sensor | **Semiestructurado** | Tiene estructura jerárquica con claves y valores, pero el esquema puede variar entre sensores o versiones; no cabe directamente en una tabla relacional. |
| Una fotografía de una máquina | **No estructurado** | Es un archivo binario (pixeles); no tiene esquema de columnas y se analiza con técnicas de visión por computadora. |
| El texto libre de un reporte de mantenimiento | **No estructurado** | Es lenguaje natural sin formato fijo; se analiza con NLP (procesamiento de lenguaje natural). |

### ¿Por qué 100,000 registros no son Big Data?

Un archivo con 100,000 filas (~4.6 MB) **cabe sin problema en la memoria RAM de una laptop común** y se procesa en segundos con pandas o incluso con Excel. Big Data no se define por una cifra fija, sino por el momento en que las herramientas tradicionales dejan de ser suficientes.

**Limitaciones al escalar:**

- Si llegan miles de sensores enviando una medición por segundo, se generarían **~86 millones de registros al día**, que ya no caben en una laptop y requerirían almacenamiento distribuido (ej. HDFS, S3).
- Procesar todo con pandas en una sola máquina se volvería lento o imposible; se necesitarían frameworks distribuidos como **Spark** o **Dask**.
- Al integrar fotos y reportes, el almacenamiento ya no puede ser relacional (necesita data lakes).
- Las alertas en tiempo real exigen procesamiento en streaming (Kafka, Spark Streaming, Flink), no batch.

---

## 7. Batch y Streaming

### Tipo de procesamiento usado en `analisis.py`

Mi programa realiza **procesamiento por lotes (batch)**. Justificación: lee un archivo completo que ya estaba guardado en disco (`sensores_industriales.csv`), procesa todos los registros de una sola vez y entrega los resultados al final. No hay flujo continuo de datos nuevos; se trata de un conjunto cerrado y estático.

### Enfoque para emitir una alerta en segundos (temp > 85 °C)

Usaría **procesamiento en streaming (tiempo real)**. Cada lectura que envía un sensor pasaría por un sistema como **Apache Kafka + Spark Streaming** (o Flink), que evalúa la condición `temperatura > 85 °C` sobre cada mensaje individualmente. Si se cumple, dispara una alerta inmediata (correo, SMS, dashboard). El criterio es que el valor de la alerta se pierde si no llega en pocos segundos.

### Enfoque para generar un resumen al terminar el día

Usaría **procesamiento por lotes (batch)**. Al final del día, un job programado leería todas las mediciones del día (ya guardadas en el data lake) y calcularía métricas agregadas: promedios, totales de alertas por planta, sensores con más fallas, etc. Aquí no importa que tarde unos minutos, porque el resumen diario no se consume al instante.

### Relación con el tiempo de necesidad

- **Alerta inmediata** → el usuario (operador de planta) la necesita en segundos para evitar daño → streaming.
- **Resumen diario** → el usuario (gerente) lo revisa al día siguiente → batch, puede tardar minutos sin problema.

---

## 8. Lambda y Kappa

### Escenario A — Lambda

La empresa quiere **combinar recálculo histórico por lotes con procesamiento rápido de mediciones recientes**. Esto corresponde a la **arquitectura Lambda**, que mantiene dos rutas paralelas: una capa batch que recalcula todo el historial periódicamente y una capa speed que procesa lo nuevo con baja latencia. La capa de servicio une ambos resultados para las consultas.

Diagrama:
                 ┌──────► [ Capa Batch ] ──────┐
                 │        (histórico)          │
   [Sensores] ───┤                             ├──► [ Capa Serving ] ──► Consultas
                 │        [ Capa Speed ]       │
                 └──────► (tiempo real) ───────┘
   [Sensores] ──► [ Log de eventos ] ──► [ Motor de streaming ] ──► [ Capa Serving ] ──► Consultas
                      (Kafka)              (Flink / Spark)

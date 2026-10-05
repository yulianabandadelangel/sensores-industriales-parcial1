# Análisis de sensores industriales

Primer parcial — **Manejo Masivo de Datos** (UPQ)
Autor: Yuliana Elizabeth Banda Del Angel
Profesor: Javier Moya

## Objetivo

Analizar las lecturas de 40 sensores industriales distribuidos en 4 plantas,
identificar alertas de temperatura y exportar los resultados para su revisión.
Se define una **alerta** cuando la temperatura es mayor que 85 °C
(regla didáctica del examen).

## Descripción de los datos

El archivo `data/sensores_industriales.csv` contiene **100,000 mediciones simuladas**
con las siguientes columnas:

| Columna          | Significado                           |
|------------------|---------------------------------------|
| id_registro      | Identificador de la medición          |
| fecha_hora       | Fecha y hora de la lectura            |
| id_sensor        | Identificador del sensor              |
| planta           | Planta donde está instalado           |
| temperatura_c    | Temperatura en grados Celsius         |
| vibracion_mm_s   | Vibración en milímetros por segundo   |

## Resultados que calcula el programa

1. Cantidad total de registros y de sensores distintos.
2. Temperatura promedio por planta.
3. Temperatura máxima registrada con el sensor y la fecha (soporta empates).
4. Cantidad de lecturas con temperatura > 85 °C.
5. Planta con más alertas (soporta empates).
6. Exporta todas las alertas a `resultados/alertas.csv`.

## Requisitos

- Python 3.10 o superior
- Las dependencias listadas en `requirements.txt`

## Instalación y ejecución

Clona el repositorio y entra a la carpeta:

```bash
git clone https://github.com/yulianabandadelangel/sensores-industriales-parcial1.git
cd sensores-industriales-parcial1
```

Crea y activa el entorno virtual:

**Windows (CMD):**
```cmd
python -m venv .venv
.venv\Scripts\activate
```

**Linux / Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instala las dependencias:

```bash
pip install -r requirements.txt
```

Ejecuta el programa:

```bash
python analisis.py
```

El programa imprime los resultados en consola y genera `resultados/alertas.csv`.

## Estructura del proyecto

```
sensores-industriales-parcial1/
├── data/
│   └── sensores_industriales.csv
├── resultados/
│   └── alertas.csv
├── evidencias/
│   └── captura_reproducibilidad.png
├── analisis.py
├── informe.md
├── README.md
├── requirements.txt
└── .gitignore
```
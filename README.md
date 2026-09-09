# Teen Mental Health - EDA con Streamlit

Este es mi proyecto final del Caso de Estudio N°4 de la Especialización en
Python for Analytics (DMC Institute). La app hace un Análisis Exploratorio
de Datos (EDA) del dataset `Teen_Mental_Health_Dataset.csv`, que tiene
información sobre hábitos digitales, descanso, actividad física e
interacción social de adolescentes, junto con variables de bienestar
(estrés, ansiedad, adicción y una etiqueta de depresión).

**Importante:** este proyecto NO hace predicciones ni diagnósticos, solo
explora y visualiza los datos. Es un trabajo educativo.

## Autor

- Nombre: Bryan Abel Pineda Sulca
- Curso: Especialización en Python for Analytics
- Año: 2026

## Capturas de la aplicación

![Pantalla Home](capturas/1_home.png)
![Carga del dataset](capturas/2_carga_datos.png)
![EDA - Info general](capturas/3_eda_info_general.png)
![EDA - Distribuciones](capturas/4_eda_distribuciones.png)
![EDA - Hallazgos clave](capturas/5_eda_hallazgos.png)

## Cómo ejecutar el proyecto

1. Clonar el repositorio:
```
git clone <link-de-tu-repositorio>
cd teen_mental_health
```

2. Instalar las dependencias:
```
pip install -r requirements.txt
```

3. Ejecutar la app:
```
streamlit run app.py
```

4. En la sección "Carga de datos" de la app, subir el archivo
`Teen_Mental_Health_Dataset.csv` que está dentro de esta misma carpeta.

## Descripción de las variables principales

| Variable | Descripción |
|---|---|
| age | Edad del adolescente (13 a 19 años) |
| gender | Género registrado |
| daily_social_media_hours | Horas diarias de uso de redes sociales |
| platform_usage | Plataforma usada: Instagram, TikTok o Both |
| sleep_hours | Horas de sueño por día |
| screen_time_before_sleep | Tiempo de pantalla antes de dormir (horas) |
| academic_performance | Indicador de rendimiento académico |
| physical_activity | Horas de actividad física |
| social_interaction_level | Nivel de interacción social: bajo, medio, alto |
| stress_level | Nivel de estrés (escala 1 a 10) |
| anxiety_level | Nivel de ansiedad (escala 1 a 10) |
| addiction_level | Nivel de dependencia / uso problemático (escala 1 a 10) |
| depression_label | Etiqueta binaria del dataset (0 = ausencia, 1 = presencia) |

## Estructura del repositorio

```
teen_mental_health/
├── app.py
├── requirements.txt
├── README.md
└── Teen_Mental_Health_Dataset.csv
```

## Links relevantes

- Repositorio GitHub: (pega aquí el link de tu repo)
- Aplicación desplegada (Streamlit Community Cloud): (pega aquí el link)

## Tecnologías usadas

Python, Pandas, NumPy, Matplotlib, Seaborn y Streamlit.

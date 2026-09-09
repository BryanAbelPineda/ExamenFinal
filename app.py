

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(page_title="Teen Mental Health - EDA", layout="wide")


# ------------------------------------------------------------
# clase que se encarga de casi todo el trabajo con los datos
# la profe pidio usar POO entonces meti las cosas principales aca
# ------------------------------------------------------------
class DataAnalyzer:
    def __init__(self, df):
        self.df = df

    # revisa que el csv tenga las columnas que esperamos, algo basico
    def validar(self):
        columnas_esperadas = [
            "age", "gender", "daily_social_media_hours", "platform_usage",
            "sleep_hours", "screen_time_before_sleep", "academic_performance",
            "physical_activity", "social_interaction_level", "stress_level",
            "anxiety_level", "addiction_level", "depression_label"
        ]
        faltan = [c for c in columnas_esperadas if c not in self.df.columns]
        if len(faltan) > 0:
            return False, faltan
        return True, []

    # separa las columnas en numericas y categoricas
    # funcion personalizada que pide el enunciado
    def clasificar_variables(self):
        numericas = []
        categoricas = []
        for col in self.df.columns:
            # uso is_numeric_dtype porque a veces el dtype sale como "object"
            # y otras veces como "str", esto funciona para los dos casos
            if pd.api.types.is_numeric_dtype(self.df[col]):
                # ojo: stress_level, anxiety_level, addiction_level y depression_label
                # son numeros pero en realidad funcionan como categorias/escalas
                numericas.append(col)
            else:
                categoricas.append(col)
        return numericas, categoricas

    def estadisticas(self):
        return self.df.describe()

    # cuenta nulos y el porcentaje, no deberia haber pero se hace igual
    def valores_faltantes(self):
        nulos = self.df.isnull().sum()
        porcentaje = (self.df.isnull().sum() / len(self.df)) * 100
        tabla = pd.DataFrame({"nulos": nulos, "porcentaje_%": porcentaje.round(2)})
        return tabla

    # filtro general, lo uso en el item 9
    def filtrar(self, edad_min, edad_max, generos, plataformas, interacciones):
        datos = self.df.copy()
        datos = datos[(datos["age"] >= edad_min) & (datos["age"] <= edad_max)]
        if len(generos) > 0:
            datos = datos[datos["gender"].isin(generos)]
        if len(plataformas) > 0:
            datos = datos[datos["platform_usage"].isin(plataformas)]
        if len(interacciones) > 0:
            datos = datos[datos["social_interaction_level"].isin(interacciones)]
        return datos


# ------------------------------------------------------------
# funciones sueltas de graficos, no las meti en la clase por flojera
# ------------------------------------------------------------
def graficar_histograma(df, columna, color="#4C72B0"):
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.histplot(df[columna], kde=True, color=color, ax=ax)
    ax.set_title(f"Distribucion de {columna}")
    st.pyplot(fig)


def graficar_barras(df, columna):
    fig, ax = plt.subplots(figsize=(5, 3))
    conteo = df[columna].value_counts()
    sns.barplot(x=conteo.index, y=conteo.values, ax=ax)
    ax.set_title(f"Conteo de {columna}")
    ax.set_ylabel("cantidad")
    st.pyplot(fig)


def graficar_boxplot(df, columna_num, columna_cat):
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.boxplot(data=df, x=columna_cat, y=columna_num, ax=ax)
    ax.set_title(f"{columna_num} segun {columna_cat}")
    st.pyplot(fig)


# ------------------------------------------------------------
# SIDEBAR - menu de navegacion
# ------------------------------------------------------------
st.sidebar.title("Menu")
opcion = st.sidebar.radio(
    "Ir a:",
    ["Home", "Carga de datos", "Analisis Exploratorio (EDA)", "Conclusiones"]
)

# esto guarda el dataframe entre pantallas, si no se pierde al cambiar de opcion
if "df" not in st.session_state:
    st.session_state.df = None


# ------------------------------------------------------------
# MODULO 1: HOME
# ------------------------------------------------------------
if opcion == "Home":
    st.title("Analisis Exploratorio: Teen Mental Health Dataset")
    st.write("""
    Este proyecto es el Caso de Estudio N4 de la Especializacion en Python for
    Analytics. La idea del proyecto es explorar el dataset de salud mental en
    adolescentes para encontrar patrones entre el uso de redes sociales, el
    descanso, la actividad fisica, la interaccion social y las variables de
    bienestar (estres, ansiedad, adiccion y la etiqueta de depresion).
    """)

    st.subheader("Datos del autor")
    st.write("Nombre completo: Bryan Abel Pineda Sulca")
    st.write("Curso / Especializacion: Especializacion en Python for Analytics")
    st.write("Año: 2026")

    st.subheader("Sobre el dataset")
    st.write("""
    El archivo Teen_Mental_Health_Dataset.csv tiene 1200 registros y 13
    columnas sobre adolescentes de 13 a 19 años. Incluye horas de uso de
    redes sociales, plataforma usada, horas de sueño, tiempo de pantalla
    antes de dormir, rendimiento academico, actividad fisica, nivel de
    interaccion social y escalas de estres, ansiedad, adiccion y una
    etiqueta binaria de depresion (depression_label).
    """)

    st.subheader("Tecnologias usadas")
    st.write("Python, Pandas, NumPy, Matplotlib, Seaborn y Streamlit.")


# ------------------------------------------------------------
# MODULO 2: CARGA DE DATOS
# ------------------------------------------------------------
elif opcion == "Carga de datos":
    st.title("Carga del dataset")
    archivo = st.file_uploader("Sube el archivo Teen_Mental_Health_Dataset.csv", type=["csv"])

    if archivo is not None:
        df = pd.read_csv(archivo)
        analizador = DataAnalyzer(df)
        ok, faltan = analizador.validar()

        if ok:
            st.success("El archivo se cargo correctamente.")
            st.session_state.df = df

            st.write("Vista previa de los datos:")
            st.dataframe(df.head())

            filas, columnas = df.shape
            col1, col2 = st.columns(2)
            col1.metric("Filas", filas)
            col2.metric("Columnas", columnas)
        else:
            st.error(f"El archivo no tiene las columnas esperadas. Faltan: {faltan}")
    else:
        st.info("Todavia no has subido el archivo csv.")


# ------------------------------------------------------------
# MODULO 3: ANALISIS EXPLORATORIO (EDA)
# ------------------------------------------------------------
elif opcion == "Analisis Exploratorio (EDA)":
    st.title("Analisis Exploratorio de Datos")

    if st.session_state.df is None:
        st.warning("Primero debes cargar el dataset en la seccion 'Carga de datos'.")
    else:
        df = st.session_state.df
        analizador = DataAnalyzer(df)

        tabs = st.tabs([
            "1. Info general", "2. Variables", "3. Estadisticas",
            "4. Faltantes", "5. Distribuciones", "6. Categoricas",
            "7. Bivariado num-cat", "8. Bivariado cat-cat",
            "9. Filtros", "10. Hallazgos"
        ])

        # ---------- ITEM 1 ----------
        with tabs[0]:
            st.header("Informacion general del dataset")
            col1, col2 = st.columns(2)
            with col1:
                st.write("Tipos de datos:")
                st.dataframe(df.dtypes.astype(str))
            with col2:
                st.write("Nulos por columna:")
                st.dataframe(df.isnull().sum())
            st.write(f"Registros duplicados: {df.duplicated().sum()}")

        # ---------- ITEM 2 ----------
        with tabs[1]:
            st.header("Clasificacion de variables")
            numericas, categoricas = analizador.clasificar_variables()
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"Variables numericas ({len(numericas)}):")
                st.write(numericas)
            with col2:
                st.write(f"Variables categoricas ({len(categoricas)}):")
                st.write(categoricas)

        # ---------- ITEM 3 ----------
        with tabs[2]:
            st.header("Estadisticas descriptivas")
            st.dataframe(analizador.estadisticas())
            st.write("""
            De forma rapida se puede ver que las medias de stress_level,
            anxiety_level y addiction_level estan mas o menos a la mitad de
            su escala (1 a 10), y que sleep_hours tiene un promedio cercano
            a las 7 horas. Con el describe tambien se ven los cuartiles que
            sirven para ver si hay valores raros o extremos.
            """)

        # ---------- ITEM 4 ----------
        with tabs[3]:
            st.header("Valores faltantes")
            tabla_nulos = analizador.valores_faltantes()
            st.dataframe(tabla_nulos)
            st.write("Como se ve en la tabla, el dataset no tiene valores nulos, por lo que no fue necesario imputar ni eliminar nada.")

        # ---------- ITEM 5 ----------
        with tabs[4]:
            st.header("Distribucion de variables numericas")
            numericas, categoricas = analizador.clasificar_variables()
            var_num = st.selectbox("Elige una variable numerica", numericas, key="hist1")
            graficar_histograma(df, var_num)

            st.write("Comparacion de escalas: stress_level, anxiety_level, addiction_level")
            col1, col2, col3 = st.columns(3)
            with col1:
                graficar_histograma(df, "stress_level", color="#DD8452")
            with col2:
                graficar_histograma(df, "anxiety_level", color="#55A868")
            with col3:
                graficar_histograma(df, "addiction_level", color="#C44E52")
            st.caption("Nota: estas escalas son autoreportadas y con fines exploratorios, no representan un diagnostico.")

        # ---------- ITEM 6 ----------
        with tabs[5]:
            st.header("Analisis de variables categoricas")
            numericas, categoricas = analizador.clasificar_variables()
            var_cat = st.selectbox("Elige una variable categorica", categoricas, key="bar1")
            col1, col2 = st.columns(2)
            with col1:
                graficar_barras(df, var_cat)
            with col2:
                proporciones = df[var_cat].value_counts(normalize=True) * 100
                st.write("Proporciones (%):")
                st.dataframe(proporciones.round(2))

        # ---------- ITEM 7 ----------
        with tabs[6]:
            st.header("Analisis bivariado (numerico vs categorico)")
            col1, col2 = st.columns(2)
            with col1:
                graficar_boxplot(df, "daily_social_media_hours", "depression_label")
            with col2:
                graficar_boxplot(df, "sleep_hours", "depression_label")

            var_extra = st.selectbox("Otra variable para comparar con depression_label",
                                      ["academic_performance", "physical_activity"])
            graficar_boxplot(df, var_extra, "depression_label")

        # ---------- ITEM 8 ----------
        with tabs[7]:
            st.header("Analisis bivariado (categorico vs categorico)")

            st.write("platform_usage vs depression_label")
            tabla1 = pd.crosstab(df["platform_usage"], df["depression_label"])
            st.dataframe(tabla1)

            st.write("social_interaction_level vs depression_label")
            tabla2 = pd.crosstab(df["social_interaction_level"], df["depression_label"])
            st.dataframe(tabla2)

            st.write("gender vs platform_usage")
            tabla3 = pd.crosstab(df["gender"], df["platform_usage"])
            st.dataframe(tabla3)

            fig, ax = plt.subplots(figsize=(6, 3))
            tabla1.plot(kind="bar", ax=ax)
            st.pyplot(fig)

        # ---------- ITEM 9 ----------
        with tabs[8]:
            st.header("Analisis dinamico con filtros")

            col1, col2 = st.columns(2)
            with col1:
                edad_min, edad_max = st.slider("Rango de edad", 13, 19, (13, 19))
                generos_sel = st.multiselect("Genero", df["gender"].unique().tolist())
            with col2:
                plataformas_sel = st.multiselect("Plataforma", df["platform_usage"].unique().tolist())
                interaccion_sel = st.multiselect("Nivel de interaccion social", df["social_interaction_level"].unique().tolist())

            datos_filtrados = analizador.filtrar(edad_min, edad_max, generos_sel, plataformas_sel, interaccion_sel)
            st.write(f"Registros despues del filtro: {len(datos_filtrados)}")

            mostrar_tabla = st.checkbox("Mostrar tabla de datos filtrados")
            if mostrar_tabla:
                st.dataframe(datos_filtrados.head(20))

            st.write("Elige una variable de bienestar y una de habitos digitales para comparar:")
            var_bienestar = st.selectbox("Variable de bienestar", ["stress_level", "anxiety_level", "addiction_level", "depression_label"])
            var_habito = st.selectbox("Variable de habitos digitales", ["daily_social_media_hours", "screen_time_before_sleep", "sleep_hours"])

            if len(datos_filtrados) > 0:
                fig, ax = plt.subplots(figsize=(6, 3))
                sns.scatterplot(data=datos_filtrados, x=var_habito, y=var_bienestar, ax=ax)
                st.pyplot(fig)
            else:
                st.write("No hay datos con esos filtros, prueba con otros.")

        # ---------- ITEM 10 ----------
        with tabs[9]:
            st.header("Hallazgos clave")

            fig, ax = plt.subplots(figsize=(6, 4))
            corr_cols = ["daily_social_media_hours", "sleep_hours", "screen_time_before_sleep",
                         "academic_performance", "physical_activity", "stress_level",
                         "anxiety_level", "addiction_level", "depression_label"]
            sns.heatmap(df[corr_cols].corr(), annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
            st.pyplot(fig)

            st.write("""
            Principales insights (esto es exploratorio, no es prediccion ni diagnostico):

            - Los adolescentes con mas horas de redes sociales tienden a tener mas
              horas de pantalla antes de dormir y algo menos de horas de sueño.
            - El grupo con depression_label = 1 muestra en promedio niveles de
              estres y ansiedad mas altos que el grupo con depression_label = 0.
            - El nivel de interaccion social bajo aparece con mas frecuencia
              relativa en el grupo con depression_label = 1.
            - No se observan diferencias muy marcadas en el uso de plataformas
              (Instagram, TikTok, Both) segun genero.
            - Estos patrones son solo asociaciones, no implican causalidad.
            """)


# ------------------------------------------------------------
# MODULO 4: CONCLUSIONES
# ------------------------------------------------------------
elif opcion == "Conclusiones":
    st.title("Conclusiones finales")

    st.markdown("""
    1. **El descanso y el uso de pantallas estan relacionados.** Se observo que a mayor
    tiempo de pantalla antes de dormir, las horas de sueño tienden a bajar un poco,
    esto se vio en el analisis bivariado del item 7.

    2. **El grupo con depression_label = 1 reporta mas estres y ansiedad.** Los
    boxplots y el heatmap de correlacion del item 10 muestran esta relacion de
    forma bastante clara.

    3. **La interaccion social baja aparece mas en el grupo etiquetado con
    depresion.** Esto se ve en la tabla cruzada del item 8
    (social_interaction_level vs depression_label).

    4. **El uso de redes sociales por si solo no explica todo.** Aunque hay
    relacion entre horas de redes y algunas variables de bienestar, la
    correlacion no es extremadamente fuerte, por lo que probablemente hay
    otros factores involucrados (familiares, academicos, etc).

    5. **No hay valores nulos ni duplicados en el dataset**, lo cual permitio
    enfocar todo el analisis en explorar distribuciones y comparar grupos
    en vez de limpiar datos.

    Estas conclusiones son de caracter exploratorio y educativo, pensadas
    para apoyar la toma de decisiones (por ejemplo, campañas de bienestar
    o programas de acompañamiento), y no deben usarse como diagnostico
    clinico ni como modelo de prediccion.
    """)

import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# ---------------------------------------------------------
# CONFIGURACIÓN DE GOOGLE SHEETS
# ---------------------------------------------------------
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

credentials = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"], scopes=scope)
gc = gspread.authorize(credentials)
sheet_id = st.secrets["google_sheet"]["sheet_id"]
sh = gc.open_by_key(sheet_id)
worksheet = sh.sheet1

# ---------------------------------------------------------
# INTERFAZ
# ---------------------------------------------------------
st.title("🧠 Cuestionario TMMS-24")
st.write("Por favor complete la siguiente encuesta de forma sincera. No hay respuestas correctas o incorrectas.")

# --- Datos sociodemográficos ---
st.header("Datos sociodemográficos")
nombre = st.text_input("Nombre completo")
correo = st.text_input("Correo electrónico")
edad = st.number_input("Edad", min_value=17, max_value=80, step=1)
genero = st.selectbox("Género", ["", "M", "F", "Otro"])
carrera = st.text_input("Carrera")
anio_ingreso = st.number_input("Año de ingreso", min_value=2000, max_value=2035, step=1)
formacion = st.radio("¿Ha recibido formación o talleres en educación socioemocional?", ["Sí", "No"])
satisfaccion = st.slider("Nivel de satisfacción con su formación emocional (1 = Muy baja, 5 = Muy alta)", 1, 5, 3)

# ---------------------------------------------------------
# PREGUNTAS TMMS-24
# ---------------------------------------------------------
st.header("Preguntas del TMMS-24")
preguntas = [
    "Presto mucha atención a los sentimientos.",
    "Normalmente me preocupo mucho por lo que siento.",
    "Normalmente dedico tiempo a pensar en mis emociones.",
    "Pienso que merece la pena prestar atención a mis emociones y estado de ánimo.",
    "Dejo que mis sentimientos afecten a mis pensamientos.",
    "Pienso en mi estado de ánimo constantemente.",
    "A menudo pienso en mis sentimientos.",
    "Presto mucha atención a cómo me siento.",
    "Tengo claros mis sentimientos.",
    "Frecuentemente puedo definir mis sentimientos.",
    "Casi siempre sé cómo me siento.",
    "Normalmente conozco mis sentimientos sobre las personas.",
    "A menudo me doy cuenta de mis sentimientos en diferentes situaciones.",
    "Siempre puedo decir cómo me siento.",
    "A veces puedo decir cuáles son mis emociones.",
    "Puedo llegar a comprender mis sentimientos.",
    "Aunque a veces me siento triste, suelo tener una visión optimista.",
    "Aunque me sienta mal, procuro pensar en cosas agradables.",
    "Cuando estoy triste, pienso en todos los placeres de la vida.",
    "Intento tener pensamientos positivos aunque me sienta mal.",
    "Si doy demasiadas vueltas a las cosas, trato de calmarme.",
    "Me preocupo por tener un buen estado de ánimo.",
    "Tengo mucha energía cuando me siento feliz.",
    "Cuando estoy enfadado intento cambiar mi estado de ánimo."
]

respuestas = []
for i, p in enumerate(preguntas, 1):
    respuestas.append(st.radio(f"{i}. {p}", [1, 2, 3, 4, 5], horizontal=True, key=f"p{i}"))

# ---------------------------------------------------------
# FUNCIÓN DE INTERPRETACIÓN
# ---------------------------------------------------------
def interpretar_tmms(sexo, atencion, claridad, reparacion):
    sexo = sexo.strip().upper()
    if sexo not in ["M", "F"]:
        return ("No especificado", "No especificado", "No especificado")

    # Atención
    if sexo == "M":
        att = "Baja atención" if atencion < 21 else "Adecuada atención" if atencion <= 33 else "Alta atención"
    else:
        att = "Baja atención" if atencion < 24 else "Adecuada atención" if atencion <= 36 else "Alta atención"

    # Claridad
    if sexo == "M":
        cla = "Baja claridad" if claridad < 25 else "Adecuada claridad" if claridad <= 36 else "Excelente claridad"
    else:
        cla = "Baja claridad" if claridad < 23 else "Adecuada claridad" if claridad <= 35 else "Excelente claridad"

    # Reparación
    if sexo == "M":
        rep = "Baja reparación" if reparacion < 23 else "Adecuada reparación" if reparacion <= 36 else "Excelente reparación"
    else:
        rep = "Baja reparación" if reparacion < 23 else "Adecuada reparación" if reparacion <= 35 else "Excelente reparación"

    return att, cla, rep

# ---------------------------------------------------------
# ENVÍO DE RESPUESTAS
# ---------------------------------------------------------
if st.button("Enviar respuestas"):
    if not (nombre and correo and genero):
        st.warning("⚠️ Por favor complete los campos obligatorios (nombre, correo y género).")
    else:
        # Calcular subescalas
        atencion = sum(respuestas[0:8])
        claridad = sum(respuestas[8:16])
        reparacion = sum(respuestas[16:24])
        att, cla, rep = interpretar_tmms(genero, atencion, claridad, reparacion)

        # Guardar fila en Google Sheets
        row = [
            nombre, correo, edad, genero, carrera, anio_ingreso,
            formacion, satisfaccion,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            atencion, claridad, reparacion,
            att, cla, rep
        ] + respuestas
        worksheet.append_row(row)

        st.success("✅ ¡Gracias! Sus respuestas fueron guardadas correctamente en Google Sheets.")
        st.info("Puede cerrar esta ventana.")

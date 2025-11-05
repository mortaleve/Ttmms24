import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Cuestionario TMMS-24")

# --- Datos sociodemográficos ---
st.header("Datos sociodemográficos")
nombre = st.text_input("Nombre completo")
correo = st.text_input("Correo electrónico")
edad = st.number_input("Edad", min_value=17, max_value=80, step=1)
genero = st.selectbox("Género", ["", "M", "F", "Otro"])
carrera = st.text_input("Carrera")
anio_ingreso = st.number_input("Año de ingreso", min_value=2000, max_value=2030, step=1)
formacion = st.radio("¿Ha recibido formación socioemocional?", ["Sí", "No"])
satisfaccion = st.slider("Nivel de satisfacción con su formación emocional", 1, 5, 3)

# --- Preguntas TMMS-24 ---
st.header("Preguntas TMMS-24")
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
    respuestas.append(st.radio(f"{i}. {p}", [1,2,3,4,5], horizontal=True, key=f"p{i}"))

# --- Botón para guardar ---
if st.button("Enviar respuestas"):
    if not (nombre and correo and genero):
        st.warning("Por favor complete todos los campos obligatorios.")
    else:
        df = pd.DataFrame([{
            "Nombre": nombre,
            "Correo": correo,
            "Edad": edad,
            "Género": genero,
            "Carrera": carrera,
            "Año_Ingreso": anio_ingreso,
            "Formación_Socioemocional": formacion,
            "Satisfacción_Formación": satisfaccion,
            "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            **{f"P{i+1}": respuestas[i] for i in range(24)}
        }])
        df.to_csv("respuestas_tmms24.csv", mode="a", header=not os.path.exists("respuestas_tmms24.csv"), index=False)
        st.success("✅ Gracias por completar el cuestionario. Sus respuestas fueron registradas.")
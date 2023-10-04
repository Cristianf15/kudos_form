from datetime import datetime 
from googleapiclient.discovery import build 
from google.oauth2 import service_account 
import gspread
import streamlit as st
import json
from PIL import Image


# Configurar el ancho de la página para que sea el ancho de la pantalla
st.set_page_config(layout="wide")

# Imagenes Index
st.session_state.kudos_logo = Image.open('img/kudos_logo.jpg')
st.session_state.pikpok_logo = Image.open('img/pikpok_logo.png')

with open("config/config.json", "r", encoding='utf-8') as archivo:
    config = json.load(archivo)

## ============================================================================================

# Autenticación con las credenciales en las APIs utilizadas
st.session_state.creds = service_account.Credentials.from_service_account_file(
    config["CREDENTIALS_FILE"], scopes=config["SCOPES"]
)

# Conexión a las API de Google Slides
st.session_state.slides_service = build("slides", "v1", credentials=st.session_state.creds)
st.session_state.drive_service = build('drive', 'v3', credentials=st.session_state.creds)
st.session_state.sheets_service = build("sheets", "v4", credentials=st.session_state.creds)

## ============================================================================================



## ============================================================================================
## ========================================= VISTA 1 ==========================================
## ======================================= Formulario =========================================
def view1():

    st.title('Formulario postulación KUDOS')
    st.write("")
    st.write("")
    st.write("")

    nombres = config["NOMBRES"]
    teams = [
        'Equipo MAMC',
        'Equipo Rival Stars Horse Racing PC',
        'Equipo Rival Stars Horse Racing VR',
        'Area ADMIN',
        'Area ART',
        'Area DEV',
        'Area IT',
        'Area QA'
    ]

    # Campo Nombre
    nombre = st.selectbox('Tu nombre:', (nombres))
    st.write("")


    # Quitar opcion anonimo y evitar autonominaciones
    nombres.extend(config["TEAMS"])

    nombres = [name for name in nombres if name != "Anónimo"]

    if nombre != "Anónimo":
        nombres = [name for name in nombres if name != nombre]

    # Campo Personas
    personas = st.multiselect(
    'Nombre de la persona, area o proyecto que quieras felicitar: :red[*]', nombres, [], placeholder="Elige una o varias opciones")
    name_error = st.empty()
    st.write("")

    # Campo Situación
    situacion = st.text_area("Situación: :red[*]")
    situation_error = st.empty()
    st.write("")

    # Valores a elegir
    valores = st.multiselect(
        "Valores a Elegir: :red[*]", 
        [
            'Be Curious',
            'Take Ownership',
            'Collaborate Well',
            'Otro'
        ],
        placeholder="Elige una o varias opciones"
    )
    valor_error = st.empty()
    st.write("")

    otro = ""
    if 'Otro' in valores:
        otro = st.text_area('Si marcaste "Otro" en la pregunta anterior y deseas complementar tu respuesta, puedes hacerlo en este espacio: ')
        if otro == "":
            otro = "n/a"

    if st.button('Enviar'):
        if personas != []:
            if situacion != "":
                if valores != []:
                    # Datos extra

                    client = gspread.authorize(st.session_state.creds)
                    sheet = client.open(config["SHEET"]).worksheet(config["WORKSHEET"])

                    # Obtener la fecha y hora actual
                    fecha_hora_actual = datetime.now().strftime('%m/%d/%Y %H:%M:%S')

                    # Crear lista para enviar
                    data_to_insert = [fecha_hora_actual, nombre, ", ".join(personas), situacion, ", ".join(valores), otro]

                    # Agregar valores a la hoja de cálculo
                    sheet.append_row(data_to_insert)

                    
                    st.session_state.current_view = "vista2"
                    st.experimental_rerun()
                    

                else:
                    valor_error.error('Por favor, elige minimo un valor.', icon="🥸")
            else:
                situation_error.error('Por favor, cuéntanos la situación, comportamiento o evento que quieres celebrar.', icon="🤓")  
        else:
            name_error.error('Por favor, elige minimo una persona o área.', icon="🧐")  

## ======================================= END VISTA 1 =======================================
## ===========================================================================================

## ============================================================================================
## ========================================= VISTA 2 ==========================================
def view2():
    st.success('Formulario enviado con exito.', icon="👍🏻")
    
    if st.button('Felicitar a alguien más'):
        st.session_state.current_view = "vista1"
        st.experimental_rerun()
## ======================================= END VISTA 2 =======================================
## ===========================================================================================

def main():

    # Crear una variable de estado para controlar la vista actual
    if "current_view" not in st.session_state:
        st.session_state.current_view = "vista1"

    # Mostrar la vista actual según el valor de la variable de estado
    if st.session_state.current_view == "vista1":
        view1()
    if st.session_state.current_view == "vista2":
        view2()

if __name__ == "__main__":
    main()
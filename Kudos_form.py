from datetime import datetime, timedelta
from googleapiclient.discovery import build 
from google.oauth2 import service_account 
import gspread
import streamlit as st
import json
from PIL import Image


from streamlit_modal import Modal

import streamlit.components.v1 as components

# Configurar el ancho de la página para que sea el ancho de la pantalla
st.set_page_config(
    page_title="Formulario Kudos PikPok", 
    page_icon='📜',
    layout="wide"
    )

# Imágenes Index
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
    col1, col2, col3 = st.columns([125, 170, 10])
    col1.title(f'¡Envía Kudos a un compañero!')

    css_styles = '''<style>
                        #info{
	                        background-color: #0E1117;
                            color: white;
                            font-family: sans-serif;
                            text-align:center;
                            width: 99%;
                        }
                        .e1f1d6gn2 > iframe{
                            background-color: #0E1117;
                            color: white;
                            font-family: sans-serif;
                        }
                        .e1f1d6gn0{
                            background-color: #0E1117;
                            color: white;
                            font-family: sans-serif;
                        }
                        .css-8542t9{
                            border: 1rem white;
                            border-top: solid;
                            border-left: solid;
                            border-bottom: solid;
                            border-radius: 10px;
                            border-right: solid;
                        }
                        .ef3psqc11 { 
                            margin-right: 3%
                        }
                    </style>
                '''
    st.markdown(css_styles, unsafe_allow_html=True)

    modal = Modal('<p style="font-size: 2rem">Info</p>', key="modal",max_width=600,padding=0)
    open_modal = col3.button("i")
    


    st.write("")
    st.write("")
    st.write("")

    nombres = config["NOMBRES"]

    # Campo Nombre
    nombre = st.selectbox('Tu nombre:', (nombres))
    st.write("")


    # Quitar opción anónimo y evitar auto-nominaciones
    nombres.extend(config["TEAMS"])

    nombres = [name for name in nombres if name != "Anónimo"]

    if nombre != "Anónimo":
        nombres = [name for name in nombres if name != nombre]

    # Campo Personas
    personas = st.multiselect(
    '¿A quién vas a felicitar?: :red[*]', nombres, [], placeholder="Elige una o más opciones")
    name_error = st.empty()
    st.write("")

    # Campo Situación
    situacion = st.text_area("Cuéntanos la situación que quieras celebrar.: :red[*]")
    situation_error = st.empty()
    st.write("")

    # Valores a elegir
    valores = st.multiselect(
        "¿Cuáles son los valores relacionados?: :red[*]", 
        [
            'Be Curious',
            'Take Ownership',
            'Collaborate Well',
            'Otro'
        ],
        placeholder="Elige una o más opciones"
    )
    valor_error = st.empty()
    st.write("")

    otro = ""
    if 'Otro' in valores:
        otro = st.text_area('¿Qué valor viste reflejado?: ')
        if otro == "":
            otro = "n/a"

    # Obtener el día actual
    day = datetime.now().day
    
    if day <= 15:
        validateMonth = st.checkbox("Este Kudos es para el mes anterior ?")
        if validateMonth:
            fecha = datetime.now()
            mesAnterior = fecha - timedelta(days=fecha.day)
            fecha_hora = mesAnterior.strftime('%m/%d/%Y %H:%M:%S')
        else:
            fecha_hora = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
    else:
        fecha_hora = datetime.now().strftime('%m/%d/%Y %H:%M:%S')


    if st.button('Enviar'):
        if personas != []:
            if situacion != "":
                if valores != []:
                    # Datos extra

                    client = gspread.authorize(st.session_state.creds)
                    sheet = client.open(config["SHEET"]).worksheet(config["WORKSHEET"])

                    # Crear lista para enviar
                    data_to_insert = [fecha_hora, nombre, ", ".join(personas), situacion, ", ".join(valores), otro]

                    # Agregar valores a la hoja de cálculo
                    sheet.append_row(data_to_insert)

                    
                    st.session_state.current_view = "vista2"
                    st.experimental_rerun()
                    

                else:
                    valor_error.error('Por favor elige un valor.', icon="🥸")
            else:
                situation_error.error('Por favor cuéntanos la situación que quieras celebrar.', icon="🤓")  
        else:
            name_error.error('Por favor elige a alguien.', icon="🧐")

    if open_modal:
        modal.open()

    if modal.is_open():
        with modal.container():
            html_string = '''
            <style>
                body{
                    margin: 0px;
                }
                .modal-content {
                    color: white;
                    font-family: sans-serif;
                    margin: 0px;
                    text-align:center;
                    padding-left: 20%;
                    line-height: 1.7;
                }
            </style>

            <p class="modal-content">
                A veces es fácil olvidar o desmeritar los pequeños logros del día a día.
                No les damos importancia porque es el "deber ser", "lo que se espera", o más burradas de esas.
                Pero siendo honestos, ¿a quién no lo motiva un comentario positivo?, ¿hay algo más reconfortante que ser felicitado por un compañero?, ¿algo mejor que un "¡sos un teso!"?
                En PikPok creemos en la importancia de celebrar nuestros logros, de felicitar a nuestros compañeros, de seguirnos impulsando hacia adelante con un mensaje de aliento.
                ¡Para eso tenemos los Kudos! Después de todo, no hay nada mejor que unas palabras de aprecio, una palmadita en el hombro, ¡o un sticker de una carita feliz!
            </p>
            
            '''
            components.html(html_string, width=500, height=390, scrolling=False) 

## ======================================= END VISTA 1 =======================================
## ===========================================================================================

## ============================================================================================
## ========================================= VISTA 2 ==========================================
def view2():
    st.success('Formulario enviado con éxito.', icon="👍🏻")
    
    if st.button('Enviar más Kudos'):
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
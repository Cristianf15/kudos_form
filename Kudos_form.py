from datetime import datetime, timedelta
from googleapiclient.discovery import build 
from google.oauth2 import service_account 
import gspread
import streamlit as st
import json
import functions as fn
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
## ========================================= Inicio ===========================================
def view1():
    col1, col2, col3 = st.columns(3)
    
    containerForm = col2.container(border=True)
    
    c1, c2, c3 = containerForm.columns([1,3,1])
    c2.image('img/Kudos_04.png')
    
    containerForm.header("",divider="rainbow")
    
    column1, column2, column3, column4 = containerForm.columns([1,2,2,1])
    
    
    if column2.button('Enviar Kudos',use_container_width=True):
        st.session_state.current_view = "vista2"
        st.rerun()

    if column3.button('Ver mis Kudos',use_container_width=True):
        st.session_state.current_view = "vista4"
        st.rerun()
## ======================================= END VISTA 1 =======================================
## ===========================================================================================

## ============================================================================================
## ========================================= VISTA 2 ==========================================
## ======================================= Formulario =========================================
def view2():
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


    # Añadir equipos a la lista de nombres
    nombres.extend(config["TEAMS"])

    # Quitar opción anónimo y evitar auto-nominaciones
    nombres = [name for name in nombres if name != "Anónimo"]
    if nombre != "Anónimo":
        nombres = [name for name in nombres if name != nombre]

    # Campo Personas
    personas = st.multiselect(
    '¿A quién vas a felicitar?: :red[*]', nombres, [], placeholder="Elige una o más opciones")
    name_error = st.empty()
    st.write("")

    # Campo Situación
    situacion = st.text_area("Cuéntanos la situación que quieras celebrar: :red[*]")
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

    # Botón enviar
    column1, column2, column3 = st.columns([2,3,20])
    if column2.button('Enviar',use_container_width=True):
        if personas != []:
            if situacion != "":
                if valores != []:
                    # Datos extra

                    client = gspread.authorize(st.session_state.creds)
                    sheet = client.open(config["SHEET"]).worksheet(config["WORKSHEET"])

                    # Crear lista para enviar
                    data_to_insert = [fecha_hora, nombre, ", ".join(personas), situacion, ", ".join(valores), otro]

                    # Agregar valores a la hoja de cálculo
                    sheet.append_row(data_to_insert,table_range="A:E")

                    
                    st.session_state.current_view = "vista3"
                    st.rerun()
                    

                else:
                    valor_error.error('Por favor elige un valor.', icon="🥸")
            else:
                situation_error.error('Por favor cuéntanos la situación que quieras celebrar.', icon="🤓")  
        else:
            name_error.error('Por favor elige a alguien.', icon="🧐")

    if column1.button('Regresar',use_container_width=True):
        st.session_state.current_view = "vista1"
        st.rerun()

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
## ======================================= END VISTA 2 =======================================
## ===========================================================================================

## ============================================================================================
## ========================================= VISTA 3 ==========================================
## =================================== Formulario Enviado =====================================
def view3():
    st.success('Formulario enviado con éxito.', icon="👍🏻")
    
    if st.button('Enviar más Kudos'):
        st.session_state.current_view = "vista2"
        st.rerun()
## ======================================= END VISTA 3 =======================================
## ===========================================================================================

## ============================================================================================
## ========================================= VISTA 4 ==========================================
## =================================== Formulario Mis Kudos ===================================
def view4():
    col1, col2, col3 = st.columns(3)
    
    containerForm = col2.container(border=True)
    
    c1, c2, c3 = containerForm.columns([1,3,1])
    c2.image('img/Kudos_04.png')

    co1, st.session_state.containerError, co1 = containerForm.columns([1,30,1])

    # Campo Nombre
    nombres = config["NOMBRES"]
    # Añadir equipos a la lista de nombres
    nombres.extend(config["TEAMS"])

    containerForm.header("",divider="rainbow")

    st.session_state.nombre = containerForm.selectbox('Tu nombre:', (nombres))
    st.write("")

    
    column1, column2, column3, column4 = containerForm.columns([1,2,2,1])
    
    if column2.button('Regresar',use_container_width=True):
        st.session_state.current_view = "vista1"
        st.rerun()

    if column3.button('Ver mis kudos',use_container_width=True):
        st.session_state.current_view = fn.validateBtnForm(config["SPREADSHEET_ID"], "vista5")
        st.rerun() 
## ======================================= END VISTA 4 =======================================
## ===========================================================================================

## ============================================================================================
## ========================================= VISTA 5 ==========================================
## ============================== Mis Kudos / Kudos Observados ================================
def view5():

    # Obtener datos de la hoja de cálculo
    range_name = "respuestas!A:E"
    result = st.session_state.sheets_service.spreadsheets().values().get(
        spreadsheetId=st.session_state.SPREADSHEET_ID, range=range_name
    ).execute()

    values = result.get("values", [])

    
    # Filtrar por nombre 
    values = fn.filter_by_name(values,st.session_state.nombre)
    if values == []:
        st.session_state.current_view = "vista4"
        main()
        st.session_state.containerError.info("¡Ups! Parece que aún no tenemos registros tuyos.", icon="🤷🏼‍♂️")
    else:
        
        # Mostrar la primera vista por defecto
        vista_seleccionada = "🏆 Kudos recibidos"

        vistas = {}

        # Slide
        vistas["🏆 Kudos recibidos"] = fn.show_kudos_history(values,st.session_state.nombre,"recibidos")

        # Gráficas
        vistas["👀 Kudos nominados"] = fn.show_kudos_history(values,st.session_state.nombre,"nominados")


        if st.sidebar.button("Regresar"):
            st.session_state.current_view = "vista4"
            st.rerun()
        st.sidebar.write("")
        st.sidebar.write("")
        st.sidebar.write("")
        st.sidebar.write("")
        
        for j in list(vistas.keys()):
            if st.sidebar.button(j):
                vista_seleccionada = j 
            st.sidebar.write("")

    
        st.sidebar.write("")
        st.sidebar.write("")
        if st.sidebar.button("Regresar al inicio"):
            st.session_state.current_view = "vista1"
            st.rerun()
                

        # Mostrar el contenido de la vista seleccionada
        vistas[vista_seleccionada]() 
## ======================================= END VISTA 5 =======================================
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
    if st.session_state.current_view == "vista3":
        view3()
    if st.session_state.current_view == "vista4":
        view4()
    if st.session_state.current_view == "vista5":
        view5()

if __name__ == "__main__":
    main()
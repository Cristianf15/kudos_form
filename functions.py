import streamlit as st
import re
import random

## ============================================================================================
def extraerID(url):
    pattern = r"/spreadsheets/d/([a-zA-Z0-9-_]+)"
    match = re.search(pattern, url)
    if match:
        return match.group(1)

    pattern = r"/presentation/d/([a-zA-Z0-9-_]+)"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None

def importFonts():
    # ----------------------------------------------------------------
    # Agregar Fuentes
    st.markdown(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap" rel="stylesheet">
        """,
        unsafe_allow_html=True,
    )
    # Agregar CSS personalizado para cambiar la fuente del texto
    st.markdown(
        """
        <style>
        /* Cambiar la fuente del texto */
        .title-text {
            font-family: 'Bebas Neue', sans-serif; 
            font-size: 28px; 
            color: #FEFEFE; 
        }

        .title-text-center {
            font-family: 'Bebas Neue', sans-serif; 
            font-size: 28px; 
            color: #FEFEFE; 
            text-align: center;
            margin-bottom: 50px
        }

        .title-text-center-arial {
            font-family: 'Arial', sans-serif; 
            font-size: 28px; 
            color: #FEFEFE; 
            text-align: center;
            margin-bottom: 50px
        }

        .normal-text {
            font-family: 'Arial', sans-serif; 
            font-size: 18px; 
            color: #FEFEFE; 
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ----------------------------------------------------------------

## ============================================================================================
## --------------------------------- Validar formulario inicio --------------------------------
## ============================================================================================
def validateBtnForm(url_GSheets,vista):
    if url_GSheets != "": 
        st.session_state.SPREADSHEET_ID = extraerID(url_GSheets)
        if st.session_state.SPREADSHEET_ID != None:
            st.session_state.current_view = vista
            st.rerun()

        else:
            if st.session_state.SPREADSHEET_ID == None:
                st.session_state.current_view = "vista4"
                st.rerun()
                st.error("¡Error! El link de Google Sheets que ingresaste no es valido, inténtalo nuevamente.", icon="🥸")

    else:
        if url_GSheets == "":
            st.session_state.current_view = "vista4"
            st.rerun()
            st.error("¡Error! Por favor ingrese un link de Google Sheets.", icon="🤓")
    
    return st.session_state.current_view
## ============================================================================================

def filter_by_name(data_values, name):
    # Filtrar las fechas del mes 7 (julio) en la columna "A" (índice 0) (data_value indica en que fila iniciará)

    filtered_data = []

    for row in data_values:
        if len(row)>=2:
            if name in row[1] or name in row[2]:
                filtered_data.append(row)

    return filtered_data

## ============================================================================================

## ============================================================================================
## -------------------------------------- Historial Kudos -------------------------------------
## ============================================================================================
def show_kudos_history(values,name,tipo): #   [1]- observador     [2]- laureado
    def kudos_history():
        if tipo == "recibidos":
            st.title(f"Mis Kudos")
            st.write("")
            st.write("")
            MyKudos = []
            containers = []

            register = [True for row in values if name in row[2]]

            if register:
                for row in values:
                    if len(row)>=2:
                        if name in row[2]:
                            MyKudos.append(row)
                            container = st.container(border=True)
                            col1, col2 = container.columns([1, 2])
                            column1, column2 = col2.columns([1, 2])

                            col1.image(f'img/Kudos_0{random.randint(1, 4)}.png')

                            column1.subheader("De:")
                            column2.write("")
                            column2.write(row[1])

                            column1.subheader("Para:")
                            column2.write("")
                            column2.write(row[2])

                            col2.write(row[3])

                            column1.subheader("Valores:")
                            column2.write("")
                            column2.write(row[4])
                            
                            containers.append(container)
                            st.write("")
            else:
                st.info("No Tienes kudos aún, pero no te desanimes. ¡Lo estás haciendo increible!✨", icon="😢")
        elif tipo == "nominados":
            st.title(f"Mis Kudos Cómo Observador")
            st.write("")
            st.write("")
            MyKudosObserved = []
            containers = []

            register = [True for row in values if row[1] == name]

            if register:
                for row in values:
                    if len(row)>=2:
                        if name in row[1]:
                            MyKudosObserved.append(row)
                            container = st.container(border=True)
                            col1, col2 = container.columns([1, 2])
                            column1, column2 = col2.columns([1, 2])

                            col1.image(f'img/Kudos_0{random.randint(1, 4)}.png')

                            column1.subheader("De:")
                            column2.write("")
                            column2.write(row[1])

                            column1.subheader("Para:")
                            column2.write("")
                            column2.write(row[2])

                            col2.write(row[3])

                            column1.subheader("Valores:")
                            column2.write("")
                            column2.write(row[4])
                            
                            containers.append(container)
                            st.write("")
            else:
                st.info("No has enviado kudos aún, manten tus ojos abiertos a los logros, aprendizajes o buenos gestos de tus compañer@s. ¡Y celebremos su esfuerzo juntos!🎉", icon="🕵🏻‍♀️")

        else:
            st.error("error en el tipo de kudos elegido(laureado o observador)")

            

    return kudos_history
## ============================================================================================
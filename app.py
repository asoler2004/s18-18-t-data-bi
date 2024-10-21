import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime
import json
#from IPython.display import IFrame

# Funcion de chat con llama

def chat_with_llama(messages):    
    API_KEY ='bb4595ff-bdaf-4dff-a0b6-ff95186f4152'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {API_KEY}"
    }
    url = 'https://api.awanllm.com/v1/chat/completions'
    
    payload = json.dumps({
        "model": "Meta-Llama-3-8B-Instruct",
        "messages": messages,
    })
    
    try:
        response = requests.post(url, headers=headers, data=payload, timeout=30)
        response.raise_for_status()  
        
        data = response.json()
        
        if 'choices' in data and data['choices']:
            return data['choices'][0]['message']['content']
        else:
            st.warning("La respuesta de la API no contiene 'choices' o está vacía.")
            st.json(data)
            return "Lo siento, no pude generar una respuesta. Por favor, inténtalo de nuevo."
    
    except requests.exceptions.RequestException as e:
        st.error(f"Error en la solicitud a la API: {e}")
        return "Lo siento, hubo un problema al comunicarse con el servicio. Por favor, inténtalo de nuevo más tarde."
    
    except json.JSONDecodeError as e:
        st.error(f"Error al decodificar la respuesta JSON: {e}")
        st.text(response.text)  # Display the raw response
        return "Lo siento, recibí una respuesta inesperada del servicio. Por favor, inténtalo de nuevo."
    
    except Exception as e:
        st.error(f"Error inesperado: {e}")
        return "Lo siento, ocurrió un error inesperado. Por favor, inténtalo de nuevo."

#Funcion de consulta a la API de la NASA

def get_fire_region(region='ESP'):
        MAP_KEY = '52dd51b587fe0f9d6bd40c412ceb4fec'
        url = f'https://firms.modaps.eosdis.nasa.gov/api/country/csv/{MAP_KEY}/MODIS_NRT/{region}/1'
        try:
            df = pd.read_csv(url, sep=',')
            return(df)
        except:
            print ("Error en la consulta.\nIntente en el navegador: %s" % url)

# Función principal de la interfaz de usuario

def main():
    st.set_page_config(
      page_title="firm-bot🔥🔥🔥",
      layout="wide",
      page_icon="🔥",
    )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    local_css("style/style.css")
    Col1,Col2 = st.columns([3,1])       
    with Col1:
        #dashboard= IFrame(src="", width=1000,height=1000)
        st.title("historic-fire-data")
    with Col2:
        st.title("firm-bot🔥🔥🔥")
        st.markdown(
            "¡hola! soy firm-bot"
        )
        # region = st.text_input("nombre de la región:")
        # mes = st.text_input("mes:")
        # anio = st.text_input("año:")

        chat_container = st.container()
        with chat_container:
            for entry in st.session_state.chat_history:
                if entry["role"] == "user":
                    st.markdown(
                        f'<div class="human-bubble">{entry["content"]}</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f'<div class="ai-bubble">{entry["content"]}</div>',
                        unsafe_allow_html=True,
                    )

        user_input = st.text_input("Indícame la región y las fechas para consultar los incendios.")
        #f"Dame información acerca de incendios en {region} en {mes} de {anio}")
        
        if st.button("enviar"):

            st.session_state.chat_history.append(
                {"role": "user", "content": user_input}            )
            previous_messages = st.session_state.chat_history 
            response = chat_with_llama(previous_messages)
            
            st.session_state.chat_history.append(
                {"role": "assistant", "content": response}
            )

            st.rerun()
if __name__ == "__main__":
    main()

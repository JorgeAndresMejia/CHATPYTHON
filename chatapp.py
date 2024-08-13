from groq import Groq
import streamlit as st 

# Iniciar el api de groq
cliente = Groq(api_key="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")

# generar un modelo y que se obtenga respuesta
def get_ai_response(messages):
    completion = cliente.chat.completions.create(
        model ="llama-3.1-70b-versatile",
        messages =messages,
        temperature = 0.7, # entre más cercano a 0 menos creativo modelo rango 0-2
        max_tokens=1024,
        stream=True,
    )   

    response = "".join(chunk.choices[0].delta.content or "" for chunk in completion)
    return response

def chat():
    st.title("Entrevista kyndryl")
    st.write("¡BIENVENIDAS Luz Esmeralda y Mary Luz. Cuando terminen de hacer sus preguntas por favor escribir 'exit' para terminar la conversación.")
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []


    #función se ejecuta cuando se da enter
    def submit():
        user_input = st.session_state.user_input
        if user_input.lower() == 'exit':
            st.write("¡gracias por convensar conmigo!")
            st.stop()

        st.session_state['messages'].append({"role": "user", "content":user_input})    

        #obteniendo respuesta   
        with st.spinner("Que pregunta tan dificil, Dame unos segundos mientras busco una respuesta..."):
            ai_response = get_ai_response(st.session_state['messages'])
            st.session_state['messages'].append({"role": "assistant", "content":ai_response})

        # Borrar input del usuario
        st.session_state.user_input = ""

    #historial del chat
    for message in st.session_state['messages']:
        role = "Luz Esmeralda y Mary Luz" if message["role"] == "user" else "BotGeorge"
        st.write(f"**{role}:** {message['content']}")

    #ingresar los datos
    with st.form(key='chat_form', clear_on_submit=True):
        st.text_input("Luz Esmeralda y Mary luz:", key="user_input")
        submit_button = st.form_submit_button(label='Enviar', on_click=submit)


if __name__== "__main__":
    chat()    
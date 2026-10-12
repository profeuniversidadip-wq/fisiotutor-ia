import os
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title='FisioTutor IA', page_icon='🎓', layout='centered')
st.title('FisioTutor IA')
st.caption('Asistente académico de Fisiología y Fisiopatología · Uso educativo')

MATERIAS = ['Fisiología general', 'Fisiopatología', 'Sistema endocrino', 'Sistema respiratorio', 'Sistema nervioso', 'Contracción muscular']
MODOS = ['Explicación guiada', 'Tutor socrático', 'Caso clínico']

with st.sidebar:
    st.header('Configuración de estudio')
    materia = st.selectbox('Asignatura o tema', MATERIAS)
    modo = st.radio('Modalidad', MODOS)
    nivel = st.selectbox('Nivel académico', ['1.º año', '2.º año', '3.º año', '4.º año'])
    if st.button('Reiniciar conversación', use_container_width=True):
        st.session_state.mensajes = []
        st.rerun()
    st.divider()
    st.caption('No ingreses datos personales ni información identificable de pacientes.')

try:
    api_key = st.secrets.get('GEMINI_API_KEY', '')
except (FileNotFoundError, KeyError):
    api_key = ''
api_key = api_key or os.getenv('GEMINI_API_KEY', '')
if not api_key:
    st.warning('Falta configurar GEMINI_API_KEY en los secretos de Streamlit. Consulta README.md.')
    st.stop()

if 'mensajes' not in st.session_state:
    st.session_state.mensajes = []

for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje['role']):
        st.markdown(mensaje['content'])

pregunta = st.chat_input('Escribe tu pregunta de fisiología...')
if pregunta:
    st.session_state.mensajes.append({'role': 'user', 'content': pregunta})
    with st.chat_message('user'):
        st.markdown(pregunta)

    instrucciones = f'''Eres FisioTutor IA, tutor universitario para carreras de la salud en Chile.
Tema: {materia}. Nivel: {nivel}. Modalidad: {modo}.
Responde en español claro, con terminología fisiológica precisa. Distingue mecanismos demostrados de hipótesis.
No inventes bibliografía ni fuentes: cuando no puedas corroborar una afirmación, dilo.
No diagnostiques ni indiques tratamiento individual a pacientes reales.
Si la modalidad es «Explicación guiada», presenta una explicación gradual y termina con una pregunta de comprobación.
Si la modalidad es «Tutor socrático», usa preferentemente preguntas secuenciales y pistas, sin revelar de inmediato toda la solución.
Si la modalidad es «Caso clínico», crea un caso hipotético educativo breve, con razonamiento por etapas y preguntas al estudiante.
Mantén las respuestas concisas. Si una explicación requiere mayor profundidad, ofrécela a petición del estudiante.
No afirmes que estás consultando libros o documentos si no se han proporcionado como contexto.
'''
    historial = '\n\n'.join(
        f"{'Estudiante' if m['role'] == 'user' else 'Tutor'}: {m['content']}"
        for m in st.session_state.mensajes[-12:]
    )
    with st.chat_message('assistant'):
        with st.spinner('Preparando respuesta...'):
            try:
                cliente = genai.Client(api_key=api_key)
                respuesta = cliente.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=historial,
                    config=types.GenerateContentConfig(system_instruction=instrucciones, temperature=0.4),
                )
                texto = respuesta.text or 'El modelo no devolvió texto. Intenta reformular la consulta.'
                st.markdown(texto)
                st.session_state.mensajes.append({'role': 'assistant', 'content': texto})
            except Exception as exc:
                st.error('No se pudo consultar Gemini. Verifica la clave, la cuota disponible y el modelo habilitado.')
                with st.expander('Detalle técnico'):
                    st.code(str(exc))

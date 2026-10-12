# FisioTutor IA

Prototipo de asistente académico universitario, desarrollado con Streamlit y Gemini.

## Instalación en Windows

1. Instala Python 3.11 o 3.12.
2. Abre una terminal en esta carpeta.
3. Ejecuta `python -m pip install -r requirements.txt`.
4. Crea `.streamlit/secrets.toml` a partir de `.streamlit/secrets.toml.example` y reemplaza el texto de ejemplo con tu propia clave de Google AI Studio.
5. Ejecuta `python -m streamlit run app.py`.

La clave de API es privada: nunca la compartas ni la subas a GitHub.

## Publicar gratuitamente sin dominio

1. Crea un repositorio en GitHub y sube `app.py`, `requirements.txt`, `.gitignore` y este README.
2. NO subas `.streamlit/secrets.toml`.
3. En https://share.streamlit.io crea una aplicación desde el repositorio.
4. En Advanced settings > Secrets pega `GEMINI_API_KEY = "tu_clave"`.
5. Despliega y comparte la URL generada con terminación `.streamlit.app`.

## Alcance

Incluye chat contextual, selector de tema, nivel y modalidad, y reinicio de sesión.
No incluye todavía base bibliográfica verificada, persistencia de resultados, autentificación de estudiantes ni controles contra uso excesivo.
Antes de abrir el servicio a muchos estudiantes, considera límites y cuotas del proveedor, mecanismos de control de acceso, privacidad y supervisión académica.
El nivel gratuito de Gemini depende del modelo y de la región; revisa https://ai.google.dev/gemini-api/docs/pricing.

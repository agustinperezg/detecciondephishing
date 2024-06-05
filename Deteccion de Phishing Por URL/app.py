import streamlit as st
import machine_learning as ml
import feature_extraction as fe
from bs4 import BeautifulSoup
import requests as re

# Utilizar el modelo RandomForest por defecto
model = ml.rf_model

# Estilo CSS
st.markdown(
    """
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #ADD8E6;
            color: #333333;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            text-align: center;
        }
        h1,
        h2 {
            color: #333333;
        }
        .image-container {
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }
        img {
            max-width: 30%;
            height: auto;
        }
        .about {
            margin: 20px 0;
            padding: 20px;
            background-color: #ADD8E6;
            border-radius: 5px;
            text-align: left;
        }
        .about-text {
            text-align: left;
        }
        .prediction {
            margin: 20px 0;
            padding: 20px;
            background-color: #ADD8E6;
            border-radius: 5px;
        }
        input,
        button {
            padding: 5px;
            font-size: 16px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Contenido HTML
st.markdown(
    """
    <div class="container">
        <h1>Pescando a los Phishers</h1>
        <div class="image-container">
            <img src="https://its.unc.edu/wp-content/uploads/sites/337/2023/10/phishing-illustration-e1696514608667.png" alt="Imagen de Phishing">
        </div>
        <div class="about">
            <h2>Acerca de:</h2>
            <p class="about-text">El phishing es una forma de ciberdelito en la que un atacante se pone en contacto con
                un objetivo a través de correo electrónico, teléfono o mensaje de texto, haciéndose pasar por una
                entidad o persona confiable. El atacante luego atrae a las personas a sitios web falsos para engañar a
                los destinatarios y obtener datos confidenciales. El propósito de esta aplicación es ayudar a
                identificar estas URLs de phishing para fomentar prácticas más seguras en línea.</p>
        </div>
        <div class="prediction">
            <h2>Predicción:</h2>
            <p>¿La URL es legítima o phishing?</p>
            <input type="text" placeholder="Ingrese la URL aquí" id="url_input">
            <button onclick="makePrediction()">Hacer Predicción</button>
            <p id="prediction_result"></p>
        </div>
    </div>
    <script>
        function makePrediction() {
            var url = document.getElementById('url_input').value;
            fetch("/predict?url=" + url)
            .then(response => response.json())
            .then(data => {
                var result = document.getElementById('prediction_result');
                if (data.prediction === 0) {
                    result.innerHTML = "Esta página web parece legítima.";
                } else {
                    result.innerHTML = "¡Atención! ¡Esta página web es un posible phishing!";
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    </script>
    """,
    unsafe_allow_html=True
)

# Proceso de verificación de la URL (funcionalidad de predicción)
@st.cache
def predict_phishing(url):
    try:
        response = re.get(url, verify=False, timeout=4)
        if response.status_code != 200:
            return None
        else:
            soup = BeautifulSoup(response.content, "html.parser")
            vector = [fe.create_vector(soup)]  # it should be 2d array, so I added []
            result = model.predict(vector)
            return result[0]
    except re.exceptions.RequestException as e:
        print("--> ", e)
        return None

# Obtener la URL ingresada por el usuario y realizar la predicción
url = st.text_input("Ingrese la URL aquí:")
if st.button("Hacer Predicción"):
    if url:
        prediction = predict_phishing(url)
        if prediction is not None:
            if prediction == 0:
                st.success("Esta página web parece legítima.")
            else:
                st.warning("¡Atención! ¡Esta página web es un posible phishing!")
        else:
            st.error("No se pudo verificar la URL. Por favor, asegúrese de que sea válida.")

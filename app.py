import streamlit as st
import requests
from PIL import Image
import io
import base64
import certifi

# Freepik API Key (Replace with your actual key)
FREEPIK_API_KEY = "FPSX78fc16b4e4cc4cb18d14771130076b61"

# Freepik Image-to-Image API Endpoint (Verify this is correct)
FREEPIK_API_URL = "https://api.freepik.com/v1/image-to-image"

# Function to encode image to base64
def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Streamlit UI
st.title("🖼️ Freepik Image-to-Image Generator")
st.write("Upload an image and enter a prompt to generate a modified version using Freepik API.")

# File uploader
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
prompt = st.text_area("Enter a prompt to modify the image", "Make the person smile with sunglasses.")

if uploaded_image and prompt:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    encoded_image = encode_image(image)

    payload = {
        "api_key": FREEPIK_API_KEY,
        "image": encoded_image,
        "prompt": prompt
    }

    if st.button("Generate Image"):
        with st.spinner("Generating image..."):
            try:
                response = requests.post(
                    FREEPIK_API_URL,
                    json=payload,
                    verify=certifi.where(),  # Use certifi's SSL certificates
                    timeout=15
                )

                if response.status_code == 200:
                    generated_image_data = response.json().get("image")

                    if generated_image_data:
                        generated_image = Image.open(io.BytesIO(base64.b64decode(generated_image_data)))
                        st.image(generated_image, caption="Generated Image", use_container_width=True)
                    else:
                        st.error("Error: No image data received from Freepik API.")
                else:
                    st.error(f"API Error: {response.status_code} - {response.text}")

            except requests.exceptions.SSLError as ssl_error:
                st.error(f"SSL Error: {ssl_error}\n\nTry updating SSL certificates.")

            except requests.exceptions.RequestException as e:
                st.error(f"Network Error: {e}")

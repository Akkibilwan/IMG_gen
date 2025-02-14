import streamlit as st
import openai
import base64
import requests
import io
import os
from PIL import Image
from dotenv import load_dotenv
import certifi

# Load environment variables
load_dotenv()

# Retrieve OpenAI API Key securely
OPENAI_API_KEY = os.getenv("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")

if not OPENAI_API_KEY:
    st.error("API key not found! Set OPENAI_API_KEY as an environment variable.")
    st.stop()

# Function to encode image to Base64
def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Function to generate an image using OpenAI DALL·E 3
def generate_image(prompt, image):
    encoded_image = encode_image(image)

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "dall-e-3",
        "prompt": prompt,
        "image": encoded_image,
        "size": "1024x1024",
        "n": 1
    }

    try:
        response = requests.post(
            "https://api.openai.com/v1/images/generations",
            headers=headers,
            json=payload,
            verify=certifi.where(),  # ✅ FIXED SSL ISSUES
            timeout=15
        )

        if response.status_code == 200:
            image_url = response.json()["data"][0]["url"]
            return image_url
        elif response.status_code == 401:
            return "⚠️ Error: Invalid API Key! Check your OpenAI API key."
        else:
            return f"⚠️ API Error: {response.status_code} - {response.text}"

    except requests.exceptions.SSLError as ssl_error:
        return f"⚠️ SSL Error: {ssl_error}. Try updating SSL certificates."

    except requests.exceptions.RequestException as e:
        return f"⚠️ Network Error: {e}"

# Streamlit UI
st.title("🖼️ DALL·E 3 Image-to-Image Generator")
st.write("Upload an image and enter a prompt to modify it using OpenAI's DALL·E 3.")

# File uploader
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
prompt = st.text_area("Enter a prompt to modify the image", "Make the person smile with sunglasses.")

if uploaded_image and prompt:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    if st.button("Generate Image"):
        with st.spinner("Generating image..."):
            generated_image_url = generate_image(prompt, image)

            if generated_image_url.startswith("http"):
                st.image(generated_image_url, caption="Generated Image", use_container_width=True)
            else:
                st.error(generated_image_url)

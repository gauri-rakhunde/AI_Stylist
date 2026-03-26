import streamlit as st
import cv2
import numpy as np
from PIL import Image
from deepface import DeepFace
import requests

# Load API keys from Streamlit secrets
openai_api_key = st.secrets["api_key"]

def analyze_facial_features(image):
    """Analyze facial features (skin tone, hair color, etc.) using DeepFace."""
    try:
        analysis = DeepFace.analyze(img_path=image, actions=["age", "gender", "race", "emotion"])
        return analysis[0]  # Return the first face analysis result
    except Exception as e:
        st.error(f"Error analyzing face: {e}")
        return None

def generate_outfit_image(facial_features, user_details):
    """Generate an outfit image using DALL-E based on facial features and user details."""
    # Create a prompt for DALL-E based on facial features and user details
    prompt = f'''Generate a realistic full-body outfit for a person with the following features:
    - Skin Tone: {facial_features['dominant_race']}
    - Gender: {user_details['gender']}
    - Age: {user_details['age']}
    - Preferred Style: {user_details['preferred_style']}
    The outfit should complement their facial features and personal style.'''

    response = requests.post(
        "https://api.openai.com/v1/images/generations",
        json={"model": "dall-e-3", "prompt": prompt, "n": 1, "size": "1024x1024"},
        headers={"Authorization": f"Bearer {openai_api_key}"}
    )

    response_data = response.json()

    if "data" in response_data and len(response_data["data"]) > 0:
        return response_data["data"][0]["url"]
    else:
        return None

# Streamlit app
st.title("Face-Based Outfit Generator")

# Upload face photo
uploaded_file = st.file_uploader("Upload a face photo", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    # Load the uploaded image
    user_image = Image.open(uploaded_file)
    st.image(user_image, caption="Uploaded Face Photo", use_container_width=True)

    # Save the image to a temporary file for DeepFace analysis
    temp_image_path = "temp_face.jpg"
    user_image.save(temp_image_path)

    # Analyze facial features
    st.write("Analyzing facial features...")
    facial_features = analyze_facial_features(temp_image_path)

    if facial_features:
        st.write("Facial analysis results:")
        st.json(facial_features)

        # Generate outfit based on facial features and user details
        if "user_details" in st.session_state:
            st.write("Generating outfit...")
            outfit_image_url = generate_outfit_image(facial_features, st.session_state.user_details)

            if outfit_image_url:
                st.image(outfit_image_url, caption="AI-Generated Outfit", use_container_width=True)
            else:
                st.error("Could not generate outfit image. Please try again.")
        else:
            st.warning("Please submit your user details first.")
    else:
        st.error("Could not analyze facial features. Please upload a clear face photo.")
import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from io import BytesIO
from PIL import Image
def generate_content(img=None):
    load_dotenv()
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-1.0-pro-vision-latest')
    try:
        response = model.generate_content([img])
        # analysis model
        model_ana = genai.GenerativeModel('gemini-1.5-pro-latest')
        prompt_ana = f'''If This results "{response.text}" do not contain any medical report data, please respond with 'Please provide me with correct data.' ONLY and do not continue. 
        Otherwise, give me the results in Arabic.'''
        response_ana = model_ana.generate_content([prompt_ana])

        return response_ana.text 
    except Exception as e:
        st.error("Failed to generate content: {}".format(e))
        return None

# Streamlit app setup

import streamlit as st
from PIL import Image
import io
def main():
    st.title("🔬🧪MedEye👩🏻‍🔬🗜️")
    st.markdown("##### Skip the Wait, Not the Detail: Fast AI Lab Analysis")

    img_file_buffer = st.file_uploader("Upload an image (jpg, png):", type=["jpg", "png"])
    img = None
    if img_file_buffer is not None:
        # Convert the file buffer to an image object
        img = Image.open(io.BytesIO(img_file_buffer.getvalue()))

    if st.button("Generate Report"):
        if img:
            # Generate content based on text and image
            processed_text = generate_content(img)
            st.markdown(f"<div style='direction: rtl; text-align: lest;'>{processed_text}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

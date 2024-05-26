import streamlit as st
import google.generativeai as gai
from api import api_key  # Ensure you have your api_key module properly set up

# Configure the generative AI API
gai.configure(api_key=api_key)

generation_config = {
    "temperature": 0.5,
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 4000,
}

system_prompt = """ 

"""

# Apply safety settings
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

# Model config
model = gai.GenerativeModel(
    model_name="gemini-pro-vision",
    safety_settings=safety_settings,
    generation_config=generation_config,
)

st.set_page_config(page_title="Vital", page_icon="")
st.image("Screenshot (59).png", width=700)

st.title("Vital image analysis")

st.subheader("Vital is a web application that utilizes AI to generate analysis reports for medical images. It does not generate images itself. It analyzes uploaded medical images, like X-rays or MRIs, and provides a comprehensive report based on the system prompt you provide. **Disclaimer:** While AI models can be helpful for medical image analysis, they should not be used for definitive diagnosis or treatment decisions. Always consult with a qualified healthcare professional.")

upload_file = st.file_uploader("Upload a medical image", type=['jpg', 'png', 'jpeg'])
if upload_file is not None:
    st.image(upload_file, caption="Uploaded Image", use_column_width=True)

submit_button = st.button("Generate Analysis")

if submit_button and upload_file is not None:
    image_data = upload_file.getvalue()
    parts = [
        {
            "mime_type": "image/jpeg",
            "data": image_data
        },
        {
            "text": system_prompt
        }
    ]
    prompt_part = {
        "parts": parts
    }

    st.title("Analysis Report")
    try:
        response = model.generate_content(prompt_part)
        st.write(response.text)
    except Exception as e:
        st.error(f"An error occurred: {e}")

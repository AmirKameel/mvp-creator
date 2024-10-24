import streamlit as st
import tempfile
import subprocess
import os
from llm_integration import generate_gpt4_code, generate_gemini_code, improve_gpt4_code, improve_gemini_code
from streamlit_navigation_bar import st_navbar

# Set up page configuration
st.set_page_config(page_title="MVP Creator", page_icon="🛠️", layout="wide")

# Define pages
pages = ["Home", "Generate", "Preview", "Improvements", "Templates"]

# Create the navigation bar
page = st.sidebar.selectbox("Select a page", pages)

# Initialize session state for generated and improved code
if 'generated_code' not in st.session_state:
    st.session_state.generated_code = ""
if 'improved_code' not in st.session_state:
    st.session_state.improved_code = ""

# Function to preview the generated app using subprocess
def preview_generated_app(code_to_run):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp_file:
        tmp_file.write(code_to_run.encode('utf-8'))
        tmp_file.flush()
        tmp_file_path = tmp_file.name

    try:
        st.info("Executing the app...")
        process = subprocess.Popen(["streamlit", "run", tmp_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if output:
            st.text_area("App Output", output.decode())
        if error:
            st.text_area("App Error", error.decode())
    except Exception as e:
        st.error(f"Error executing app: {str(e)}")
    finally:
        os.remove(tmp_file_path)

# Function to list available templates
def list_templates():
    templates = [f for f in os.listdir("./templates") if f.endswith(".py")]
    return templates

# Home Page
if page == "Home":
    st.title("Welcome to the AI-Powered MVP/PoC App Creator")
    st.markdown("Create your app idea using AI models!")

# Generate Page
elif page == "Generate":
    st.title("Generate Your App")
    app_idea = st.text_area("Describe your app idea", placeholder="I want an app for a custom GPT on my data")
    llm_model = st.selectbox("Choose LLM Model", ["GPT-4 (OpenAI)", "Gemini (Google)"])

    if st.button("Generate App"):
        if app_idea:
            with st.spinner("Generating your app..."):
                if llm_model == "GPT-4 (OpenAI)":
                    st.session_state.generated_code = generate_gpt4_code(app_idea)
                elif llm_model == "Gemini (Google)":
                    st.session_state.generated_code = generate_gemini_code(app_idea)
                st.success("App successfully generated!")
                st.code(st.session_state.generated_code, language='python')

# Preview Page
elif page == "Preview":
    st.title("Preview Your App")
    code_to_preview = st.session_state.generated_code
    if code_to_preview:
        if st.button("Preview App"):
            preview_generated_app(code_to_preview)
    else:
        st.warning("No code available. Please generate an app first.")

# Improvements Page
elif page == "Improvements":
    st.title("Request Improvements")
    improvement_request = st.text_area("What improvements do you want to request?", placeholder="Add error handling or change the layout...")
    
    if st.button("Apply Improvements"):
        if improvement_request:
            with st.spinner("Applying improvements..."):
                if st.session_state.generated_code:
                    st.session_state.improved_code = improve_gpt4_code(st.session_state.generated_code, improvement_request)
                    st.success("Improvements applied!")
                    st.code(st.session_state.improved_code, language='python')
                else:
                    st.warning("No code available to improve.")
        else:
            st.warning("Please describe the improvements you want.")

# Templates Page
elif page == "Templates":
    st.title("App Templates")
    templates = list_templates()
    selected_template = st.selectbox("Available Templates", templates)

    if selected_template:
        template_path = os.path.join("./templates", selected_template)
        with open(template_path, "r") as file:
            template_code = file.read()
            st.code(template_code, language='python')

        if st.button("Run Template"):
            preview_generated_app(template_code)

import streamlit as st
import tempfile
import subprocess
import os
from llm_integration import generate_gpt4_code, generate_gemini_code, improve_gpt4_code, improve_gemini_code
from streamlit_navigation_bar import st_navbar

# Set up page configuration
st.set_page_config(page_title="MVP Creator", page_icon="$", layout="wide")

# Define pages and their respective URLs with icons
pages = [("🏠 Home", "Home"), ("⚙️ Generate", "Generate"), ("👁️ Preview", "Preview"), ("🔧 Improvements", "Improvements"), ("📂 Templates", "Templates"), ("A_Eye", "A_Eye")]
urls = {"A_Eye": "https://github.com/gabrieltempass/streamlit-navigation-bar"}

# Styles for the navigation bar
styles = {
    "nav": {
        "background-color": "#2C3E50",  # Dark blue
        "justify-content": "center",
        "padding": "1px",
        "border-radius": "5px",
        "box-shadow": "0px 4px 8px rgba(0,0,0,0.2)"
    },
    "img": {
        "padding-right": "14px",
    },
    "span": {
        "color": "white",
        "font-weight": "bold",
        "padding": "14px",
        "font-size": "18px"
    },
    "active": {
        "background-color": "white",
        "color": "#2C3E50",
        "font-weight": "bold",
        "padding": "14px",
        "border-radius": "5px",
        "box-shadow": "0px 4px 8px rgba(0,0,0,0.1)"
    }
}
options = {
    "show_menu": False,
    "show_sidebar": True,
}

# Create the navigation bar
page = st_navbar(
    [name for name, label in pages],
    urls=urls,
    styles=styles,
    options=options,
)


# Initialize session state for generated code and improvements
if 'generated_code' not in st.session_state:
    st.session_state.generated_code = ""
if 'improved_code' not in st.session_state:
    st.session_state.improved_code = ""

# Function to preview the generated or improved app using subprocess
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

# Folder where templates are stored
TEMPLATES_DIR = "./templates"

# Function to list available templates
def list_templates():
    templates = [f for f in os.listdir(TEMPLATES_DIR) if f.endswith(".py")]
    return templates

# Function to preview selected template
def preview_template(template_name):
    template_path = os.path.join(TEMPLATES_DIR, template_name)
    
    with open(template_path, "r") as file:
        code = file.read()
    
    # Display the code of the template
    st.code(code, language='python')
    
    # Option to run and preview the app
    if st.button(f"Run {template_name}"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp_file:
            tmp_file.write(code.encode('utf-8'))
            tmp_file.flush()
            tmp_file_path = tmp_file.name

        try:
            st.info(f"Running {template_name}...")
            process = subprocess.Popen(["streamlit", "run", tmp_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()

            if output:
                st.text_area("App Output", output.decode())
            if error:
                st.text_area("App Error", error.decode())
        except Exception as e:
            st.error(f"Error running template: {str(e)}")
        finally:
            os.remove(tmp_file_path)

# Sidebar navigation
with st.sidebar:
    st.title("Navigation")
    st.subheader("Sections")
    selected_section = st.selectbox("Choose an option", ["Home", "Generate App", "Preview", "Improvements", "Templates"])


# Main content based on selected section
if selected_section == "Home" or page == "Home":
    st.title("Welcome to the AI-Powered MVP/PoC App Creator")
    
    # CSS for modern, colorful blocks
    st.markdown("""
        <style>
        .feature-box {
            background: linear-gradient(135deg, #89CFF0, #4169E1); /* Gradient for a premium feel */
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            color: white;
            font-weight: bold;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        }
        .header {
            font-size: 24px;
            font-family: 'Trebuchet MS', sans-serif;
        }
        .subheader {
            font-size: 18px;
            font-family: 'Verdana', sans-serif;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="feature-box"><h3 class="header">✨ Unlock the Magic of Creation!</h3></div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="feature-box">
            <p class="subheader">Welcome to your very own genie, a mystical AI-powered app creator! With just a flick of your wand (or a click of your mouse), you can transform your dreams into reality...</p>
        </div>
    """, unsafe_allow_html=True)

elif selected_section == "Generate App" or page == "Generate":
    st.title("Step 1: Generate Your App")
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

elif selected_section == "Preview" or page == "Preview":
    st.title("Preview Your App")
    code_to_preview = st.session_state.improved_code if st.session_state.improved_code else st.session_state.generated_code
    if code_to_preview:
        st.download_button("Download App Code", code_to_preview, file_name="app_code.py")
        if st.button("Preview App"):
            preview_generated_app(code_to_preview)
    else:
        st.warning("No code available. Please generate an app or apply improvements first.")

elif selected_section == "Improvements" or page == "Improvements":
    st.title("Request Improvements")
    llm_model = st.selectbox("Choose LLM Model", ["GPT-4 (OpenAI)", "Gemini (Google)"])
    improvement_request = st.text_area("What improvements do you want to request?", placeholder="Add error handling or change the layout...")

    if st.button("Apply Improvements"):
        if improvement_request:
            with st.spinner("Applying improvements..."):
                if llm_model == "GPT-4 (OpenAI)":
                    st.session_state.improved_code = improve_gpt4_code(st.session_state.generated_code, improvement_request)
                elif llm_model == "Gemini (Google)":
                    st.session_state.improved_code = improve_gemini_code(st.session_state.generated_code, improvement_request)
                st.success("Improvements applied!")
                st.code(st.session_state.improved_code, language='python')
                st.download_button("Download Improved App Code", st.session_state.improved_code, file_name="improved_app.py")
        else:
            st.warning("Please describe the improvements you want.")

# Your main code
elif selected_section == "Templates" or page == "Templates":
    st.title("App Templates")
    templates = list_templates()

    if templates:
        template_name = st.selectbox("Available Templates", templates)
        if template_name:
            st.subheader(f"Previewing Template: {template_name}")
            preview_template(template_name)

            # Read and display the original template code
            with open(os.path.join(TEMPLATES_DIR, template_name), "r") as file:
                original_code = file.read()

            # Display the original code of the selected template
            # st.code(original_code, language='python')

            st.write("### Suggest Improvements")
            improvements = st.text_area("Describe your improvements for this app", placeholder="E.g., Add a new feature or improve UI...")

            if st.button("Submit Improvements"):
                if improvements:
                    # Use GPT-4 to improve the code based on user input
                    with st.spinner("Applying improvements..."):
                        improved_code = improve_gpt4_code(original_code, improvements)

                    # Store the improved code in session state
                    st.session_state.improved_code = improved_code

                    st.success("Improvements applied! Here is the improved code:")
                    st.code(improved_code, language='python')

            # Option to preview the improved app (only if improved code is available)
            if 'improved_code' in st.session_state:
                if st.button("Preview Improved App"):
                    preview_generated_app(st.session_state.improved_code)

    else:
        st.warning("No templates found.")



# Adding CSS for premium feel
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Montserrat', sans-serif;
    }
    .stButton>button {
        background-color: #FFD700;
        color: #2C3E50;
        font-size: 18px;
        padding: 10px 20px;
        border-radius: 8px;
        border: none;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.2);
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #FFC300;
        box-shadow: 0px 6px 12px rgba(0,0,0,0.3);
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #2C3E50;
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 14px;
    }
    @keyframes fadeIn {
        from {opacity: 0;}
        to {opacity: 1;}
    }
    .animated {
        animation: fadeIn 1s ease-in;
    }
    </style>
    """, unsafe_allow_html=True)

# Custom footer
st.markdown("""
    <div class="footer">
        <p>Created by Amir Kameel | <a href="https://linkedin.com/in/yourprofile" style="color: #FFD700;">LinkedIn</a> | <a href="https://github.com/yourgithub" style="color: #FFD700;">GitHub</a></p>
    </div>
""", unsafe_allow_html=True)

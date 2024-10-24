import streamlit as st
import openai
import toml

# Load the secrets from the toml file
secrets = toml.load('secrets.toml')

# Create the OpenAI client using the API key from secrets.toml
client = openai.OpenAI(api_key=secrets['openai']['api_key'])

# Streamlit app setup
st.set_page_config(
    page_title="GPT-4o Text Generation",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Main header
st.title("Custom GPT-4o Text Generation App")
st.subheader("Enter your prompt below to generate text using GPT-4o.")

# User input area
prompt = st.text_area("Your prompt:", "", height=150, placeholder="Type your prompt here...")

# Generate text with improved UI
if st.button("Generate Text 🚀"):
    if prompt:
        with st.spinner("Generating response..."):
            try:
                # Request completion from GPT-4o
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}]
                )
                
                # Display the generated text
                st.success("Generated Text:")
                st.markdown(f"```{response.choices[0].message.content}```")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a prompt to generate text.")
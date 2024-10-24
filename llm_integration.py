import openai
import os
import toml 
import openai
import google.generativeai as genai
import os
import streamlit as st

def generate_gpt4_code(user_idea):
    openai_api_key = st.secrets["openai"]["api_key"]
    client = openai.OpenAI(api_key=openai_api_key)

    # Prepare the system message to instruct GPT to generate Streamlit apps with LLM integration
    system_message = """
    You are an expert in building MVP (Minimum Viable Product) applications using Streamlit and various language models (LLMs). 
    Given a specific LLM to use, you will create a Streamlit app that integrates with the LLM for text generation based on user input. 
    Below are examples of how to use different LLMs in the generated code.
    Do not include markdown "```" or "```python" at the start or end. 
    if the llm selected is gpt use the same structure as i will send like this (client.chat.completions.create) and the model gpt-4o then return response.choices[0].message.content
    read the openai api key exact like this  
    # Load the secrets 
    openai_api_key = st.secrets["openai"]["api_key"]
    client = openai.OpenAI(api_key=openai_api_key)

    # Create the OpenAI client using the API key from secrets.toml
    client = openai.OpenAI(api_key=secrets['openai']['api_key'])
    """

    # User prompt for the app idea
    user_message = f"Create an app for: {user_idea}. The app should integrate gpt4o for text generation, handling user input, and displaying results."

    # Prepare messages for the OpenAI API
    messages = [
        {
            'role': 'system',
            'content': system_message  # System message that sets the instructions
        },
        {
            'role': 'user',
            'content': user_message  # User's app idea
        }
    ]

    # OpenAI API request for chat completion
    response = client.chat.completions.create(
        model='gpt-4o',  # Specify the model (GPT-4 in this case, or 'gpt-3.5-turbo' if needed)
        messages=messages,
        max_tokens=4000,  # Adjust as per requirements
        temperature=0.7,  # Adjust for creativity vs. accuracy
        top_p=1.0  # Adjust for randomness in response generation
    )

    # Extract the generated code from the API response
    generated_code = response.choices[0].message.content
    return generated_code




def generate_gemini_code(user_idea):
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompt = f"Create a Streamlit app for: {user_idea}. The app should integrate Gemini for text generation."

    response = model.generate_content(prompt)

    generated_code = response.text
    return generated_code



# Function to apply improvements to generated code based on user feedback
def improve_gpt4_code(generated_code, improvement_request):
    openai_api_key = st.secrets["openai"]["api_key"]
    client = openai.OpenAI(api_key=openai_api_key)

    system_message = f"""
    You are an expert in Python, Streamlit integration. 
    Here's the original code for a generated app:
    
    {generated_code}

    Now, apply the following improvements to the code:

    {improvement_request}

    Make sure the updated app works as expected.
    Do not include markdown "```" or "```python" at the start or end. just reply with the full code without any text as explaination or something
    """
    user_message = f"{improvement_request}"

    # Prepare messages for the OpenAI API
    messages = [
        {
            'role': 'system',
            'content': system_message  # System message that sets the instructions
        },
        {
            'role': 'user',
            'content': user_message  # User's app idea
        }
    ]


    # Send request to LLM for code improvement
    response = client.chat.completions.create(
        model="gpt-4o",  # Adjust for different models as needed
        messages=messages,
        max_tokens=4000
    )

    return response.choices[0].message.content


# Gemini Code Improvement
def improve_gemini_code(generated_code, improvement_request):
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
    Improve the following code for a Streamlit app that uses Gemini:

    {generated_code}

    Improvement request: {improvement_request}
    Do not include markdown "```" or "```python" at the start or end. just reply with the full code without any text as explaination or something

    """

    response = model.generate_content(prompt)
    improved_code = response.text
    return improved_code

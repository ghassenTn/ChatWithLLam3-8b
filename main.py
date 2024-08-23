import streamlit as st
import ollama
import io
import sys

# Sidebar for model selection
with st.sidebar:
    st.markdown("## Model Settings")
    desire_model = st.text_input("Model Name", value="llama3.1:8b")
    st.markdown("[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)")
    st.markdown("[![Open in GitHub Codespaces](https://github.com/codespaces.new/streamlit/llm-examples?quickstart=1)]")

# Initialize Streamlit app
st.title("💬 LLaMA 3.1 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by LLaMA 3.1")

# Check if session state has been initialized
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Display chat messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Input for user prompt
if prompt := st.chat_input("Enter your question:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Placeholder for progressive response display
    response_placeholder = st.empty()

    # Call Ollama API and get response
    with st.spinner("Thinking..."):
        response = ollama.chat(desire_model, messages=st.session_state.messages)
        response_content = response["message"]["content"]

    # Add the response to session state
    st.session_state.messages.append({"role": "assistant", "content": response_content})
    st.chat_message("assistant").write(response_content)

    # Display and execute the response if it's Python code
    if "```python" in response_content:
        st.write("### Executing the generated Python code:")
        
        # Extract the code block
        code_block = response_content.split("```python")[1].split("```")[0]
        
        # Display the code
        st.code(code_block, language="python")
        
        # Execute the code block and capture output
        with st.spinner("Executing..."):
            old_stdout = sys.stdout
            redirected_output = sys.stdout = io.StringIO()
            try:
                exec(code_block)
                exec_output = redirected_output.getvalue()
            except Exception as e:
                exec_output = str(e)
            finally:
                sys.stdout = old_stdout

        # Display execution result
        st.code(exec_output)

   

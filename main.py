from matplotlib import pyplot as plt
import streamlit as st
import ollama
import io
import sys
import plotly.graph_objects as go  # Import Plotly
import pandas as pd
# Sidebar for model selection
with st.sidebar:
    st.markdown("## Model Settings")
    desire_model = st.text_input("Model Name", value="llama3.1:8b", disabled=True)
    st.markdown("[View the source code](https://github.com/ghassenTn/ChatWithLLam3-8b/blob/main/main.py)")

st.caption("🚀 A Streamlit chat powered by ghassen using LLaMA 3.1")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Enter your question:"):
    st.session_state.messages.append({"role": "user", "content":f"{prompt} without description" })
    st.chat_message("user").write(prompt)
    response_placeholder = st.empty()
    with st.spinner("Thinking..."):
        response = ollama.chat(desire_model, messages=st.session_state.messages)
        response_content = response["message"]["content"]

    st.session_state.messages.append({"role": "assistant", "content": response_content})
    # st.chat_message("assistant").write(response_content)

    if "```python" in response_content:
        st.write("### Executing the generated Python code:")
        
        code_block = response_content.split("```python")[1].split("```")[0]
        
        st.code(code_block, language="python")
        
        with st.spinner("Executing..."):
            old_stdout = sys.stdout
            redirected_output = sys.stdout = io.StringIO()
            try:
                exec(code_block)
                exec_output = redirected_output.getvalue()

                # If a Plotly chart was created
                if 'fig' in locals():  
                    with st.expander("Plotly Chart", expanded=True):
                        st.plotly_chart(fig)  
                elif 'sns' in locals():
                    with st.expander("Seaborn Chart", expanded=True):
                        st.pyplot(plt)  # Display Seaborn chart directly in Streamlit
                elif 'plt' in locals():
                    with st.expander("Matplotlib Chart", expanded=True):
                        st.pyplot(plt)
                else:
                    st.write("No Plotly figure was generated.")

            except Exception as e:
                exec_output = str(e)
            finally:
                sys.stdout = old_stdout

        st.code(exec_output)

        # Clear the current figure after displaying it
        plt.clf()  # Clear the figure
    st.write(response_content)

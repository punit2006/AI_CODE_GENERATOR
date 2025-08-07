import streamlit as st
import os
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq

st.title("Groq-Powered Code Generator with Suggestions")

st.write("""
This application uses the Groq API to generate code based on your task and language specifications.
You can also get suggestions for the generated code and iterate on it.
""")

# Ensure task and language inputs are always available
task = st.text_area("Enter your coding task:", key='task_input')
language = st.text_input("Enter the programming language:", key='language_input')

# Assume the API key is available as an environment variable or Streamlit secret
# Use st.secrets for better security in Streamlit Cloud
try:
    groq_api_key = st.secrets["MYNAME"]
except KeyError:
    groq_api_key = os.getenv("MYNAME")

if not groq_api_key:
    st.error("GROQ_API_KEY not found. Please set it in your environment variables or Streamlit secrets.")
else:
    # Define and initialize LLM
    llm = ChatGroq(
        temperature=0,
        model_name="llama3-8b-8192",
        groq_api_key=groq_api_key
    )

    # Define code generation prompt
    code_prompt = PromptTemplate(
        input_variables=["language", "task"],
        template="""
You are an expert programmer AI tasked with generating clean, efficient, and well-commented code in {language}.

**Task:** {task}

**Instructions:**
- Write efficient, readable code with meaningful comments.
- Ensure it can be executed without errors.
- Provide sample output for the code if applicable.
- If assumptions are made, list them as comments.
- End with a short explanation of why {language} is suitable for this task.
- Give them 2 points about the improvements in the program.
"""
    )

    # Create LLMChain for code generation
    code_chain = LLMChain(llm=llm, prompt=code_prompt)

    # Define suggestion prompt
    suggestion_prompt = PromptTemplate(
        input_variables=["code", "language", "task"],
        template="""
You are an expert code reviewer AI.

Here is the task: {task}
Language: {language}

Here is the current generated code:
```{language}
{code}
""" )

    # Create LLMChain for suggestions
    suggestion_chain = LLMChain(llm=llm, prompt=suggestion_prompt)


    # Button to trigger initial code generation
    if st.button("Generate Code", key='generate_initial_code_button'):
        if task and language:
            with st.spinner("Generating code..."):
                generated_code = code_chain.run(task=task, language=language)
                st.session_state.generated_code = generated_code
                st.session_state.task = task # Store task and language in state
                st.session_state.language = language
                if 'suggestions' in st.session_state:
                     del st.session_state.suggestions # Clear old suggestions
            st.subheader("Generated Code:")
            st.code(st.session_state.generated_code, language=st.session_state.language)
        else:
            st.warning("Please enter both a coding task and a programming language.")

    # Display generated code if already exists in session state
    if 'generated_code' in st.session_state:
        st.subheader("Current Code:")
        # Use language from session state for syntax highlighting
        st.code(st.session_state.generated_code, language=st.session_state.language)

        # Options for further interaction
        st.subheader("Choose your next action:")
        option = st.radio(
            "Select an option:",
            ('Get suggestions', 'Generate code with suggestions', 'Edit the code manually', 'Generate another code', 'Let the model make a change you define', 'Exit/Final Code'),
            key='user_option'
        )

        # Handle option logic based on the selected option
        if option == 'Get suggestions':
            if 'suggestions' not in st.session_state: # Only generate if not already present
                 with st.spinner("Generating suggestions..."):
                    suggestions = suggestion_chain.run(
                        code=st.session_state.generated_code,
                        language=st.session_state.language, # Use language from state
                        task=st.session_state.task # Use task from state
                    )
                    st.session_state.suggestions = suggestions
            st.subheader("Suggested Improvements:")
            st.info(st.session_state.suggestions)

        elif option == 'Generate code with suggestions':
            if 'suggestions' in st.session_state:
                st.subheader("Generating code with suggestions...")
                # Use task and language from state
                updated_task = f"{st.session_state.task}\n\nIncorporate the following suggestions:\n{st.session_state.suggestions}"
                with st.spinner("Generating updated code..."):
                    generated_code = code_chain.run(task=updated_task, language=st.session_state.language)
                    st.session_state.generated_code = generated_code
                    # Task in state is updated to include suggestions for continuity if needed
                    st.session_state.task = updated_task
                    if 'suggestions' in st.session_state:
                        del st.session_state.suggestions # Clear old suggestions after incorporating
                st.subheader("Updated Code:")
                st.code(st.session_state.generated_code, language=st.session_state.language)
            else:
                st.warning("Please get suggestions first before generating code with suggestions.")

        elif option == 'Edit the code manually':
            st.subheader("Edit the code below:")
            # Use code from state, store edits back to state
            edited_code = st.text_area("Edit Code", value=st.session_state.generated_code, height=400, key='edited_code_area')
            if st.button("Apply Manual Edits"):
                st.session_state.generated_code = edited_code
                st.success("Code updated with your manual changes.")
                # No rerun needed, Streamlit handles update on button click

        elif option == 'Generate another code':
            st.subheader("Generate Another Code:")
            # Provide new input fields for task and language
            new_task = st.text_area("Enter the new coding task:", key='another_task_input')
            new_language = st.text_input("Enter the new programming language:", key='another_language_input')
            if st.button("Generate New Code"):
                if new_task and new_language:
                    with st.spinner("Generating new code..."):
                        generated_code = code_chain.run(task=new_task, language=new_language)
                        st.session_state.generated_code = generated_code
                        st.session_state.task = new_task # Update task and language in state
                        st.session_state.language = new_language
                        if 'suggestions' in st.session_state:
                             del st.session_state.suggestions # Clear old suggestions
                    st.subheader("Newly Generated Code:")
                    st.code(st.session_state.generated_code, language=st.session_state.language)
                else:
                    st.warning("Please enter both a new coding task and a programming language.")


        elif option == 'Let the model make a change you define':
            st.subheader("Request a Custom Change:")
            custom_change = st.text_area("Describe the change you want the model to make:", key='custom_change_input')
            if st.button("Apply Custom Change"):
                if custom_change:
                     # Append custom change to the existing task from state
                    updated_task_with_custom = f"{st.session_state.task}\n\nUpdate Request: {custom_change}"
                    with st.spinner("Applying custom change..."):
                        generated_code = code_chain.run(task=updated_task_with_custom, language=st.session_state.language)
                        st.session_state.generated_code = generated_code
                        st.session_state.task = updated_task_with_custom # Update task in state
                        if 'suggestions' in st.session_state:
                            del st.session_state.suggestions # Clear old suggestions
                    st.subheader("Code with Custom Change:")
                    st.code(st.session_state.generated_code, language=st.session_state.language)
                else:
                    st.warning("Please describe the custom change you want.")

        elif option == 'Exit/Final Code':
            st.subheader("Final Code Output:")
            if 'generated_code' in st.session_state:
                st.code(st.session_state.generated_code, language=st.session_state.language)
            else:
                st.info("No code has been generated yet.")
            st.write("Exiting... Have a productive coding session!")

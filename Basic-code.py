!pip install -U langchain-groq -U langchain-community pypdf pypdf2 sentence-transformers faiss-cpu wikipedia google-search-results

# ✅ Groq-Powered Code Generator with Suggestions in One Cell

# Install required packages (if not already installed)
!pip install --quiet langchain langchain-groq

# ✅ All-in-One Script Starts Here
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq

try:
    from google.colab import userdata
except ImportError:
    raise ImportError("⚠️ This script is designed to run in Google Colab with secrets managed via 'google.colab.userdata'.")

# ✅ STEP 1: Load API key
groq_api_key = userdata.get("MYNAME")  # Replace 'MYNAME' with your key alias in Colab secrets
if not groq_api_key:
    raise ValueError("❌ 'MYNAME' not found in Colab secrets. Use: userdata.set('MYNAME', 'your_groq_api_key')")

# ✅ STEP 2: Initialize LLM
llm = ChatGroq(
    temperature=0,
    model_name="llama3-8b-8192",
    groq_api_key=groq_api_key
)

# ✅ STEP 3: Code generation prompt
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

# ✅ STEP 4: Suggestion prompt
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

#STEP 5: Chain setup
code_chain = LLMChain(llm=llm, prompt=code_prompt)
suggestion_chain = LLMChain(llm=llm, prompt=suggestion_prompt)

#STEP 6: User Input
task = input("📝 Enter your coding task: ")
language = input("💻 Enter the programming language: ")

generated_code = code_chain.run(task=task, language=language)
print("\n✅ Generated Code:\n")
print(generated_code)

import re

# ✅ Split suggestion text into list
def parse_suggestions(text):
    # Split on numbered list (e.g. 1. or 1️⃣) using regex
    parts = re.split(r"\n\s*(?:\d[\.:️⃣])\s*", text.strip())
    return [s.strip() for s in parts if s]

while True:
    choice = input("\n🤖 What would you like to do next?\n"
                   "1️⃣ Get suggestions for the code\n"
                   "2️⃣ Generate code with suggestions\n" # New option added here
                   "3️⃣ Edit the code manually\n"
                   "4️⃣ Generate another code\n"
                   "5️⃣ Let the model make a change you define\n"
                   "6️⃣ Exit\n" # Updated exit option number
                   "Enter 1, 2, 3, 4, 5, or 6: ").strip() # Updated input prompt

    if choice == "1":
        # ✅ Generate and print suggestions
        suggestions = suggestion_chain.run(code=generated_code, language=language, task=task)
        print("\n💡 Suggested Improvements:\n")
        print(suggestions)

    elif choice == "2": # New option functionality
        print("\n🔄 Generating code with suggestions...")
        # Assuming 'suggestions' variable holds the last generated suggestions
        if 'suggestions' in locals() and suggestions:
            updated_task = f"{task}\n\nIncorporate the following suggestions:\n{suggestions}"
            generated_code = code_chain.run(task=updated_task, language=language)
            print("\n✅ Updated Code:\n")
            print(generated_code)
        else:
            print("❌ No suggestions available yet. Please select option 1 first.")

    elif choice == "3": # Updated option number
        print("\n🔧 Edit the code below. When you're done, copy and paste it back here.")
        print("-" * 30)
        print(generated_code)
        print("-" * 30)
        edited_code = input("Paste your edited code here: ")
        generated_code = edited_code # Update the generated_code with the user's edited version
        print("\n✅ Code updated with your manual changes.")


    elif choice == "4": # Updated option number
        # ✅ Get new user input and generate code again
        task = input("📝 Enter your new coding task: ")
        language = input("💻 Enter the programming language for the new task: ")
        generated_code = code_chain.run(task=task, language=language)
        print("\n✅ Generated Code:\n")
        print(generated_code)

    elif choice == "5": # Updated option number
        custom = input("🔧 Enter the change you want the model to make: ")
        task += f"\n\nUpdate Request: {custom}" # Add the custom request to the task for the model

        # ✅ Regenerate updated code
        generated_code = code_chain.run(task=task, language=language)
        print("\n🔁 Updated Code based on your request:\n")
        print(generated_code)

    elif choice == "6": # Updated exit option number
        print("\n✅ Final Code Output:\n")
        print(generated_code)
        print("\n👋 Exiting... Have a productive coding session!")
        break

    else:
        print("❌ Invalid input. Please enter 1, 2, 3, 4, 5, or 6.") # Updated invalid input message


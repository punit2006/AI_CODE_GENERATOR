# AI_CODE_GENERATOR
An intelligent code generation tool powered by Groq API and LLaMA 3 model that generates high-quality code and provides improvement suggestions.

## Features

- 🤖 **Smart Code Generation**: Generate clean, efficient code based on task descriptions and programming languages
- 💡 **Code Improvement Suggestions**: Receive expert code review and optimization recommendations
- ✏️ **Code Editing**: Manually edit code or request specific modifications from the model
- 🔄 **Iterative Optimization**: Integrate suggestions into regenerated code
- 🌐 **Web Interface**: User-friendly Streamlit application
- 🔗 **Remote Access**: Public URL access via ngrok

## Technology Stack

- **Language**: Python
- **Core Framework**: LangChain
- **AI Model**: Groq LLaMA 3 (llama3-8b-8192)
- **Web Interface**: Streamlit
- **Remote Access**: ngrok

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/ai-code-generator.git
cd ai-code-generator
```

### 2. Install Dependencies

```bash
pip install -U langchain-groq langchain-community pypdf pypdf2 sentence-transformers faiss-cpu wikipedia google-search-results streamlit pyngrok
```

### 3. Set Up API Key

#### Method 1: Environment Variable

```bash
export MYNAME="your_groq_api_key_here"
```

#### Method 2: Streamlit Secrets File

1. Create `.streamlit` directory:
   ```bash
   mkdir -p .streamlit
   ```

2. Create `.streamlit/secrets.toml` file:
   ```toml
   MYNAME = "your_groq_api_key_here"
   ```

## Usage

### In Google Colab

1. Open the [Google Colab notebook](https://colab.research.google.com/drive/1uhOg_LiZFyQl9QdQ3Jgu1k77I9pQNyU_#scrollTo=dda97322_)
2. In Colab's "Secrets" panel, add a secret named `MYNAME` with your Groq API key
3. Run all cells

### Local Streamlit Application

1. Ensure API key is set (as described above)
2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

3. Access the application at `http://localhost:8501`

### Remote Access with ngrok

1. Set your ngrok auth token:
   ```bash
   ngrok config add-authtoken YOUR_NGROK_AUTHTOKEN
   ```

2. Run the provided script to start the app with ngrok tunnel:
   ```bash
   python ai_code_generator_(2).py
   ```

3. Access the application at the public URL displayed in the console

## How to Use

1. **Generate Code**:
   - Enter your coding task description
   - Specify the programming language
   - Click "Generate Code"

2. **Get Suggestions**:
   - After code generation, select "Get suggestions"
   - Review the improvement recommendations

3. **Improve Code**:
   - Select "Generate code with suggestions" to regenerate with improvements
   - Or choose "Edit the code manually" for direct editing
   - Or use "Let the model make a change you define" for specific modifications

4. **Iterate**:
   - Generate new code for different tasks
   - Apply multiple rounds of suggestions and improvements

5. **Finalize**:
   - Select "Exit/Final Code" to see your final code
   - Copy the code for use in your projects

## Security Note

- **API Key**: Never share your Groq API key or commit it to version control
- **Secrets Management**: Use environment variables or Streamlit secrets for secure key storage
- **ngrok Token**: Keep your ngrok auth token private

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Acknowledgments

- Powered by [Groq](https://groq.com/) API
- Built with [LangChain](https://langchain.com/)
- UI powered by [Streamlit](https://streamlit.io/)
- Remote access via [ngrok](https://ngrok.com/)
- Original Colab notebook: (https://colab.research.google.com/drive/1uhOg_LiZFyQl9QdQ3Jgu1k77I9pQNyU_#scrollTo=dda97322)

# Setup

## Create virtual environment and activate it; then install the required dependecies inside venv
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

## Install Ollama CLI and the pull the SLM llama3:8b
ollama pull llama3:8b

## Run the application
streamlit run app.py - GUI
OR
python main.py - CLI
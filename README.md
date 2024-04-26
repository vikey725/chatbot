# A simple Chatbot using gpt 3.5, llama_index, langchain, and streamlit

## Instructions

1. Clone the repo
   ```
   git clone https://github.com/vikey725/chatbot.git
   ```
2. get into chatbot directory
   ```
   cd chatbot
   ```
3. Make a file .env, and put your OpenAI API key in it
   ```
   OPENAI_API_KEY = <Your_Open_AI_key>
   ```
4. create conda environment using provided environment.yml
   ```
   conda env create -f environment.yml
   ```
5. Activate the environment
   ```
   conda activate chatbot
   ```
6. Edit configs.py as per instruction provided in it
7. Run the web crawler
   ```
   python web_crawler.py
   ```
8. Run chatbot
   ```
   streamlit run main.py
   ```


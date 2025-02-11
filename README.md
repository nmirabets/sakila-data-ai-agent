# 🤖 Sakila Data AI Agent 📊

A powerful AI-powered chatbot that helps you analyze and query the Sakila database (a sample MySQL database representing a DVD rental store) using natural language. Built with OpenAI's GPT models, Python, and Streamlit.

## 🌟 Features

- Natural language querying of the Sakila database
- Interactive chat interface built with Streamlit
- Powered by OpenAI's GPT models
- SQL query generation from natural language questions
- Comprehensive database schema understanding

## 🛠️ Prerequisites

- Python 3.x
- MySQL with Sakila database installed
- OpenAI API key
- Required Python packages (see Installation section)

## 📦 Fork, Clone, Install, Add environment variables and Run

1. Fork, Clone the repository:
```bash
git clone https://github.com/yourusername/sakila-data-ai-agent.git
cd sakila-data-ai-agent
```

2. Install required packages:
```bash
pip install openai streamlit pymysql sqlalchemy python-dotenv
```

3. Set up your environment variables:
   - Copy `.env.sample` to `.env`
   - Add your OpenAI API key and database credentials to `.env`:
```
OPENAI_API_KEY=your_api_key_here
DB_PASSWORD=your_database_password
```

## 🚀 Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided local URL
3. Start chatting with the AI agent about the Sakila database!

## 💡 Example Queries

You can ask questions like:
- "How many movies are in the database?"
- "What are the most rented movies?"
- "Show me the top 10 customers by rental count"
- "What's the average rental duration?"

## 🗄️ Project Structure

- `app.py`: Main Streamlit application
- `agent/`: Directory containing agent-related modules
  - `agent.py`: Core agent implementation
  - `tools.py`: Database querying tools
  - `prompts.py`: System prompts
  - `sakila_schema.py`: Database schema information
- `Guide.ipynb`: Jupyter notebook with detailed implementation guide
- `.env.sample`: Sample environment variables file

## 🔧 Technical Details

The project combines several key technologies:
- OpenAI API for natural language understanding and SQL generation
- Streamlit for the web interface
- SQLAlchemy for database interactions
- MySQL (Sakila database) for data storage

The agent uses a sophisticated system prompt that includes the complete Sakila database schema, allowing it to generate accurate SQL queries based on natural language questions.

## 📚 Understanding the Implementation

To understand how this project is built, check out the `Guide.ipynb` notebook in the repository. The guide walks through the complete implementation process, including:
- Setting up the OpenAI API
- Creating system prompts
- Implementing tool calls
- Building the database querying functionality
- Developing the Streamlit interface

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

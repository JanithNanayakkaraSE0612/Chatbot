import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import openai
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

# Load API keys
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)  # Enable CORS

# Initialize LangChain AI model 
llm = ChatOpenAI(model_name="gpt-3.5-turbo")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    # Generate AI response
    response = llm([HumanMessage(content=user_input)])
    return jsonify({"response": response.content})

if __name__ == "__main__":
    app.run(debug=True)

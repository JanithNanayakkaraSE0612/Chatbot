import os
from flask import Flask, render_template, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
# from flask_cors import CORS
# from dotenv import load_dotenv
# import openai
# from langchain.chat_models import ChatOpenAI
# from langchain.schema import HumanMessage

# Load API keys
# load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
# CORS(app)  # Enable CORS

# Initialize LangChain AI model 
# llm = ChatOpenAI(model_name="gpt-3.5-turbo")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["GET","POST"])
def chat():
    data = request.form["msg"]
    user_input = data
    return get_Chat_response(user_input)

    # if not user_input:
    #     return jsonify({"error": "No input provided"}), 400

    # Generate AI response
    # response = llm([HumanMessage(content=user_input)])
    # return jsonify({"response": response.content})
def get_Chat_response(text):
    for step in range(5):
    # encode the new user input, add the eos_token and return a tensor in Pytorch
     new_user_input_ids = tokenizer.encode(str(text) + tokenizer.eos_token, return_tensors='pt')

    # append the new user input tokens to the chat history
    bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids

    # generated a response while limiting the total chat history to 1000 tokens, 
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

    # pretty print last ouput tokens from bot
    return tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

if __name__ == "__main__":
    app.run(debug=True)
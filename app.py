from flask import Flask, render_template, request
from chatbot import ChatBot
app = Flask(__name__)

c = ChatBot()

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['user_input']
    response = c.query_matching(user_query=user_input)
    return response

if __name__ == '__main__':
    app.run(debug=True)
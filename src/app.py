from flask import Flask, request, jsonify, render_template
from mail_assistant import MailAssistant
from create_chat_answer import create_chat_answer

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    message = data['message']

    mail_assistant = MailAssistant()
    parsed_data = mail_assistant.parse_mail(message)
    none_str, gened_mail = mail_assistant.gen_mail(message, parsed_data)
    print(parsed_data)
    print(gened_mail)
    answer = create_chat_answer(parsed_data, gened_mail)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
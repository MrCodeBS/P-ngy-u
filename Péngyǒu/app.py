from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    # Add your logic here to generate a response based on the user input
    response = "Hello! I'm Péngyǒu. How can I help you?"
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)

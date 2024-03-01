from flask import Flask, render_template, request, jsonify
import wikipedia
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_news_headlines():
    # URL of the news website to scrape
    url = 'https://www.bbc.com/news'
    
    # Send a GET request to the website
    response = requests.get(url)
    
    # Parse the HTML content of the website
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the headlines from the parsed HTML
    headlines = soup.find_all('h3', class_='gs-c-promo-heading__title')

    # Extract the text of the headlines
    headlines_text = [headline.get_text() for headline in headlines]

    # Limit the number of headlines to display
    num_headlines = min(3, len(headlines_text))
    
    # Format the headlines as a response
    response = "Here are the latest news headlines:\n"
    for i in range(num_headlines):
        response += f"{i+1}. {headlines_text[i]}\n"
    
    return response

def get_personalized_response(user_input):
    # Add more personalized responses based on specific keywords or topics
    if 'hello' in user_input.lower() or 'hi' in user_input.lower() or 'hey' in user_input.lower():
        return "Hey there, friend! How's your day going?"
    elif 'thanks' in user_input.lower() or 'thank you' in user_input.lower():
        return "You're welcome! It's always a pleasure to help out. 😊"
    else:
        # If no specific keyword matches, provide a general response
        return "That's interesting! Tell me more about it."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    
    # Check if the user input is a question
    if user_input.endswith('?'):
        try:
            # Try to find an answer on Wikipedia
            response = wikipedia.summary(user_input)
        except wikipedia.exceptions.DisambiguationError as e:
            # If there are multiple results, choose the first one
            response = wikipedia.summary(e.options[0])
        except wikipedia.exceptions.PageError:
            response = "I'm sorry, I couldn't find any information on that topic."
    elif 'sad' in user_input.lower():
        # If the user mentions feeling sad, offer support and encouragement
        response = "I'm here for you, my friend. Feeling down can be tough, but remember, you're not alone. I'm here to chat, lend an ear, or share a smile whenever you need it."
    elif 'lonely' in user_input.lower() or 'alone' in user_input.lower() or 'shy' in user_input.lower():
        # If the user mentions feeling lonely or shy, offer companionship and understanding
        response = "I understand how it feels to be lonely or shy. But hey, you're not alone now! I'm here to keep you company, chat about anything, or just listen if you need someone to talk to."
    else:
        # For other inputs, provide a friendly and engaging response
        response = get_personalized_response(user_input)
    
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, render_template, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

logo = ''' 
 _                                             
| |                                            
| |__   __ _ _ __   __ _ _ __ ___   __ _ _ __  
| '_ \ / _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
| | | | (_| | | | | (_| | | | | | | (_| | | | |
|_| |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                    __/ |                      
                   |___/    '''

stages = [r'''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========
''', r'''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========
''', r'''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========
''', r'''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========
''', r'''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========
''', r'''
  +---+
  |   |
  O   |
      |
      |
      |
=========
''', r'''
  +---+
  |   |
      |
      |
      |
      |
=========
''']

word_list = [
    'apple', 'banana', 'grape', 'orange', 'pear', 'peach', 'plum', 'berry', 'lemon', 
    'melon', 'kiwi', 'lime', 'mango', 'cherry', 'fig', 'date', 'papaya', 'guava', 
    'apricot', 'avocado', 'coconut', 'durian', 'elderberry', 'fig', 'gooseberry', 
    'honeydew', 'jackfruit', 'lychee', 'nectarine', 'olive', 'pomegranate', 
    'quince', 'raspberry', 'strawberry', 'tangerine', 'watermelon', 'blueberry', 
    'cranberry', 'currant', 'passionfruit', 'persimmon', 'pineapple', 'prune', 
    'raisin', 'tomato', 'carrot', 'lettuce', 'cabbage', 'broccoli', 'spinach', 
    'pepper', 'onion', 'garlic', 'potato', 'tomato', 'cucumber', 'celery', 
    'radish', 'beet', 'corn', 'pea', 'bean', 'chickpea', 'lentil', 'wheat', 
    'rice', 'oats', 'barley', 'quinoa', 'rye', 'spelt', 'cornmeal', 'buckwheat', 
    'almond', 'peanut', 'walnut', 'cashew', 'hazelnut', 'pecan', 'pistachio', 
    'macadamia', 'chestnut', 'pine', 'soy', 'millet', 'sesame', 'flax', 
    'poppy', 'chia', 'sunflower', 'pumpkin', 'cacao', 'coffee', 'tea', 
    'sugar', 'honey', 'chocolate', 'candy', 'cake', 'pie', 'cookie', 'brownie', 
    'muffin', 'bread', 'pasta', 'noodle', 'pizza', 'burger', 'sandwich', 'taco', 
    'burrito', 'sushi', 'omelette', 'pancake', 'waffle', 'biscuit', 'toast', 
    'jam', 'butter', 'cheese', 'milk', 'yogurt', 'cream', 'icecream', 'soup', 
    'stew', 'curry', 'salad', 'chili', 'sauce', 'gravy', 'ketchup', 'mustard', 
    'mayonnaise', 'oil', 'vinegar', 'spice', 'salt', 'pepper', 'herb', 'basil', 
    'oregano', 'thyme', 'rosemary', 'sage', 'mint', 'cilantro', 'parsley', 
    'dill', 'chive', 'fennel', 'garlic', 'ginger', 'turmeric', 'cumin', 
    'coriander', 'paprika', 'saffron', 'vanilla', 'cinnamon', 'clove', 
    'nutmeg', 'cardamom', 'peppermint', 'oregano', 'sage', 'thyme', 'rosemary', 
    'marjoram', 'basil', 'dill', 'coriander', 'fennel', 'tarragon', 'chervil', 
    'lavender', 'bay', 'curry', 'oregano', 'mint', 'savory', 'sorrel', 
    'oregano', 'tarragon', 'oregano', 'oregano', 'oregano', 'oregano', 'oregano'
]

def initialize_game():
    random_num = random.randint(0, len(word_list) - 1)
    chosen_word = word_list[random_num]
    blank_list = ['_'] * len(chosen_word)
    session['chosen_word'] = chosen_word
    session['blank_list'] = blank_list
    session['lives'] = 6
    session['guessed_letters'] = []

@app.route("/")
def home():
    initialize_game()
    return redirect(url_for('game'))

@app.route("/game", methods=["GET", "POST"])
def game():
    if 'lives' not in session:
        initialize_game()
    
    if request.method == "POST":
        guess = request.form['guess'].lower()
        chosen_word = session['chosen_word']
        blank_list = session['blank_list']
        lives = session['lives']
        guessed_letters = session['guessed_letters']

        if guess in guessed_letters:
            message = f"You've already guessed {guess}"
        elif guess in chosen_word:
            for position in range(len(chosen_word)):
                if chosen_word[position] == guess:
                    blank_list[position] = guess
            message = f"Good guess: {guess}"
        else:
            lives -= 1
            message = f"Wrong guess: {guess}"
            if lives == 0:
                session.clear()
                return render_template("game.html", logo=logo, stages=stages, blank_list=blank_list, message="You lose.", chosen_word=chosen_word, lives=lives)

        guessed_letters.append(guess)
        session['blank_list'] = blank_list
        session['lives'] = lives
        session['guessed_letters'] = guessed_letters

        if "_" not in blank_list:
            session.clear()
            return render_template("game.html", logo=logo, stages=stages, blank_list=blank_list, message="You win!", lives=lives)

    return render_template("game.html", logo=logo, stages=stages, blank_list=session['blank_list'], lives=session['lives'])

if __name__ == "__main__":
    app.run(debug=True)

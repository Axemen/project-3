from flask import Flask, jsonify, render_template, send_file, request
from keras.models import load_model
import pickle
import numpy as np


app = Flask(__name__)

def load_keras_model():
    """Load in the pre-trained model"""
    global keras_model
    keras_model = load_model('static/models/keras_model.h5')
    keras_model._make_predict_function()
    global vectorizer
    # with open('static/models/tfidf.pickle', 'rb') as f:
    #     vectorizer = pickle.load(f)

    

    

# render out an index page
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/model", methods = ['POST', 'GET'])
def model():
    errors = []
    results = []
    user_input = 'input something'
    if request.method == 'POST':
        try: 
            user_input = request.form['user_input']
            print(user_input)
        except Exception as e:
            errors.append("it didn't work...")

    # prediction = session['prediction']
    return render_template('model.html', errors = errors, results = results, text = user_input)

@app.route('/predict', methods = ['POST', 'GET'])
def predict():
    user_input = request.form.get('url')
    categories = ['Single Malt Scotch',
                  'Flavored Whiskey and Liqueurs',
                  'Bourbon',
                  ' Blended Malt Scotch Whisky ',
                  'Blended Scotch Whisky',
                  'Blended Whiskey (Multi-country)',
                  ' Single Malt Whisky (Multi-country)',
                  ' Single Grain Whisky (Multi-country)',
                  'Japan',
                  ' Canada',
                  'Irish',
                  'Generic Whisky (Multi-country)',
                  'Rye Whisky',
                  'White Whisky',
                  'Craft Whisky']
    with open('static/models/tfidf.pickle', 'rb') as f:
        vectorizer = pickle.load(f)
    keras_model = load_model('static/models/keras_model.h5')
    keras_model._make_predict_function()
    
    v_input = vectorizer.transform([user_input])
    predictions = keras_model.predict(v_input)
    max_index = np.argmax(predictions)
    output = categories[max_index]

    return render_template('index.html/#model', text = output)

if __name__ == "__main__":
    # load_keras_model()
    app.run()

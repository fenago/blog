from flask import Flask, request, render_template
import numpy as np
import pickle

app = Flask(__name__)

#app.config['UPLOAD_FOLDER'] = './data'
categorical_to_string = {
    0: 'Not a spam',
    1: 'Its a spam'
}

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        review = request.form.get('review')

        model = pickle.load(open('model.pkl', 'rb'))
        vectorizer = pickle.load(open("vector.pkl", "rb"))

        transformed_review = vectorizer.transform([review])
        model_prediction = categorical_to_string[model.predict(transformed_review)[0]]

        return render_template('index.html', prediction={'review': review, 'prediction': model_prediction})

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port=80)

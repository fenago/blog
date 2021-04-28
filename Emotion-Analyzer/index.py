from flask import Flask, request, render_template
from clean_and_train import predict
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = './data'

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']

        filename = secure_filename(file.filename)

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        file.save(file_path)
        
        predicted_label = predict(file_path, 'saved_models/Emotion_Voice_Detection_Model.h5')
        return render_template('index.html', label={'label': predicted_label[0]})
    return render_template('index.html')

    
if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port=80)
from flask import Flask, request, render_template
import sys
from cosine_similarity import calc_cosine_sim
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = './data'

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file_1 = request.files['file_1']
        file_2 = request.files['file_2']

        filename_1 = secure_filename(file_1.filename)
        filename_2 = secure_filename(file_2.filename)

        file1_path = os.path.join(app.config['UPLOAD_FOLDER'], filename_1)
        file2_path = os.path.join(app.config['UPLOAD_FOLDER'], filename_2)

        file_1.save(file1_path)
        file_2.save(file2_path)
        
        cosine_sim = calc_cosine_sim(file1_path, file2_path)
        return render_template('index.html', similarity={'cosine': cosine_sim})
    return render_template('index.html')

    
if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port=80)

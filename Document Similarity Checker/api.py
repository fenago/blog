from flask import Flask, request, jsonify
import sys
from cosine_similarity import calc_cosine_sim

app = Flask(__name__)

@app.route("/api/calc_cosine", methods=['GET'])
def api_calc_cosine():
    file1_path = request.args.get('file_1')
    file2_path = request.args.get('file_2')
    cosine_sim = calc_cosine_sim(file1_path, file2_path)
    return jsonify(f'The cosine similarity is {cosine_sim}')

    
if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port=80)
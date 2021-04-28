from flask import Flask, request, jsonify
import sys
from clean_and_train import predict

app = Flask(__name__)

@app.route("/api/predict_emotion", methods=['GET'])
def api_calc_cosine():
    file_path = request.args.get('file_path')
    predicted_label = predict(file_path, 'saved_models/Emotion_Voice_Detection_Model.h5')
    return jsonify(f'The predicted label is {predicted_label[0]}')

    
if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port=80)
from flask import Flask, request, jsonify
from me_bot import speak_like_me, respond_like_me

app = Flask(__name__)

@app.route("/api/speak", methods=['GET'])
def api_respond():
    query = request.args.get('query')
    sentences = speak_like_me(query, 2)
    return jsonify('The output sentences are {}'.format(sentences))

@app.route("/api/respond", methods=['GET', 'POST'])
def api_speak():
    query = request.args.get('query')
    sentences = respond_like_me(query, 2)
    return jsonify('The output sentences are {}'.format(sentences))

    
if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port=80, threaded=False)

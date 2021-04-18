from flask import Flask, request, render_template
from me_bot import speak_like_me, respond_like_me

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form.get("query")
        respond_sents = respond_like_me(query, 2)
        speak_sents = speak_like_me(query, 2)

        return render_template("index.html", sentences={'respond': respond_sents, 'speak': speak_sents})
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port=80)
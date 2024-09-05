from flask import Flask, render_template, jsonify, request
from recommendations import (
    find_similar_books_by_author,
    find_similar_books_by_publisher,
    get_id_from_partial_name,
    recommend_books_by_average_rating,
    
)
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

app = Flask(__name__)

# Initialize ChatterBot
chatbot = ChatBot('Booky',read_only=False,
    logic_adapters=[
      {
                    "import_path":"chatterbot.logic.BestMatch",
                    "default_response":"Sorry I don't have an answer",
                    "maximum_similarity_threshold": 0.7
      }
      
      ])        

trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")

@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/recommendations/<case>", methods=["POST"])
def recommendations(case):
    if request.method == "POST":
        query = request.json.get("query")
        case = str(case)
        case = case.strip()
        if case == "1":
            result = find_similar_books_by_author(query)
            return jsonify(result)
        elif case == "2":
            result = find_similar_books_by_publisher(query)
            return jsonify(result)
        elif case == "3":
            result = get_id_from_partial_name(query)
            return jsonify(result)
        elif case == "4":
            result = recommend_books_by_average_rating(num_recommendations=int(query))
            return jsonify(result)
        
        else:
            return jsonify("Invalid Input or invalid case number")

@app.route("/chat", methods=["POST"])
def chat():
    if request.method == "POST":
        user_input = request.json.get("query")
        bot_response = chatbot.get_response(user_input)
        return jsonify(str(bot_response))

if __name__ == "__main__":
    app.run(debug=True)
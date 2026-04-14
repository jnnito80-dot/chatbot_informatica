from flask import Flask, request, jsonify

app = Flask(__name__)

faq = {
    "¿cuándo es la evaluación del primer grado?": "La evaluación de 1° será en la última semana de mayo.",
    "¿cuándo es la evaluación del segundo grado?": "La evaluación de 2° será en la primera semana de junio.",
    "¿cuándo es la evaluación del tercer grado?": "La evaluación de 3° será en la segunda semana de junio.",
    "¿cuándo son los exámenes de recuperación?": "Los exámenes de recuperación serán en la primera semana de julio."
}

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").lower()
    response = faq.get(user_message, "Lo siento, aún no tengo respuesta para esa pregunta.")
    return jsonify({"reply": response})

@app.route("/")
def home():
    return "¡Hola! El chatbot escolar está funcionando."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

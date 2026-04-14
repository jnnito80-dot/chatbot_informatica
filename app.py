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
    return """
    <html>
      <head>
        <style>
          body { font-family: Arial; margin: 0; padding: 0; }
          #chatbox { border:1px solid #ccc; border-radius:10px; width:100%; height:100%; display:flex; flex-direction:column; }
          #messages { flex:1; padding:10px; overflow-y:auto; }
          .msg { margin:5px 0; padding:8px; border-radius:8px; max-width:80%; }
          .user { background:#d1e7dd; align-self:flex-end; }
          .bot { background:#f8d7da; align-self:flex-start; }
          #inputArea { display:flex; border-top:1px solid #ccc; }
          #inputArea input { flex:1; padding:10px; border:none; border-radius:0; }
          #inputArea button { padding:10px; border:none; background:#007bff; color:white; }
        </style>
      </head>
      <body>
        <div id="chatbox">
          <div id="messages"></div>
          <div id="inputArea">
            <input id="message" placeholder="Escribe tu pregunta...">
            <button onclick="sendMessage()">Enviar</button>
          </div>
        </div>
        <script>
          async function sendMessage() {
            const msg = document.getElementById("message").value;
            if (!msg) return;
            addMessage(msg, "user");
            document.getElementById("message").value = "";
            const res = await fetch('/chat', {
              method: 'POST',
              headers: {'Content-Type': 'application/json'},
              body: JSON.stringify({message: msg})
            });
            const data = await res.json();
            addMessage(data.reply, "bot");
          }
          function addMessage(text, type) {
            const div = document.createElement("div");
            div.className = "msg " + type;
            div.innerText = text;
            document.getElementById("messages").appendChild(div);
            div.scrollIntoView();
          }
        </script>
      </body>
    </html>
    """

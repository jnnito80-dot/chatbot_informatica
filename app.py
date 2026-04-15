from flask import Flask, request, jsonify

app = Flask(__name__)

faq = {
    "¿cuándo es la evaluación del primer grado?": "La evaluación de 1° será en la última semana de mayo.",
    "¿cuándo es la evaluación del segundo grado?": "La evaluación de 2° será en la primera semana de junio.",
    "¿cuándo es la evaluación del tercer grado?": "La evaluación de 3° será en la segunda semana de junio.",
    "¿cuándo son los exámenes de recuperación?": "Los exámenes de recuperación serán en la primera semana de julio."
    "¿cuándo es la evaluación del tercer trimestre?": "Del 8 al 12 de junio."
    "¿cuál es la liga de la guía de primer grado?": "https://bit.ly/4gYbYGs"
    "¿cuál es la liga de la guía de segundo grado?": "https://bit.ly/473bNoZ"
    "¿cuál es la liga de la guía de tercer grado?": "https://bit.ly/4nDryK5"
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
          body { font-family: 'Segoe UI', sans-serif; margin:0; padding:0; background-color:#eef5ff; }
          #chatbox { border:2px solid #4285f4; border-radius:10px; width:100%; height:100%; display:flex; flex-direction:column; background-color:#ffffff; }
          #header { background:#4285f4; color:white; padding:10px; display:flex; justify-content:space-between; align-items:center; }
          #messages { flex:1; padding:10px; overflow-y:auto; background-color:#f9fbff; }
          .msg { margin:5px 0; padding:10px; border-radius:8px; max-width:80%; font-size:0.95em; }
          .user { background:#4285f4; color:#fff; align-self:flex-end; }
          .bot { background:#ffeb3b; color:#000; align-self:flex-start; }
          #inputArea { display:flex; border-top:1px solid #ccc; background-color:#eef5ff; }
          #inputArea input { flex:1; padding:10px; border:none; background-color:#fff; color:#000; }
          #inputArea button { padding:10px; border:none; background:#4285f4; color:white; cursor:pointer; font-weight:bold; }
          #inputArea button:hover { background:#3064c9; }
          #minimizeBtn { cursor:pointer; font-weight:bold; }
        </style>
      </head>
      <body>
        <div id="chatbox">
          <div id="header">
            <span>🤖 Chatbot Escolar</span>
            <span id="minimizeBtn">—</span>
          </div>
          <div id="messages"></div>
          <div id="inputArea">
            <input id="message" placeholder="Escribe tu pregunta...">
            <button onclick="sendMessage()">Enviar</button>
          </div>
        </div>
        <script>
          // Mensaje de bienvenida automático
          window.onload = function() {
            addMessage("¡Hola! Bienvenido al Chatbot de Informática. Pregúntame sobre evaluaciones o exámenes.", "bot");
          };

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

          // Botón minimizar dentro del chat
          document.getElementById("minimizeBtn").addEventListener("click", function() {
            document.getElementById("chatbox").style.display = "none";
          });
        </script>
      </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

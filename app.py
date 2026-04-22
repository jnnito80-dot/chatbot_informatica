from flask import Flask, request, jsonify
import json
import difflib

app = Flask(__name__)

with open("faq.json", "r", encoding="utf-8") as f:
    faq = json.load(f)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").lower()

    # Buscar coincidencia exacta
    if user_message in faq:
        response = faq[user_message]
    else:
        # Buscar coincidencia más cercana
        posibles = difflib.get_close_matches(user_message, faq.keys(), n=1, cutoff=0.6)
        if posibles:
            response = faq[posibles[0]]
        else:
            response = "Lo siento, aún no tengo respuesta para esa pregunta."

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
            <span>🤖 Chatbot T56</span>
          </div>
          <div id="messages"></div>
          <div id="inputArea">
            <input id="message" placeholder="Escribe tu pregunta...">
            <button onclick="sendMessage()">Enviar</button>
          </div>
        </div>
        <script>
            function addMessage(text, type) {
                const div = document.createElement("div");
                div.className = "msg " + type;

                // 1. Reemplazar saltos de línea por <br>
               // 2. Convertir enlaces en clicables
                const formatted = text
                  .replace(/\n/g, "<br>")
                  .replace(/(https?:\/\/\S+)/g, '<a href="$1" target="_blank">$1</a>');

                div.innerHTML = formatted;
                document.getElementById("messages").appendChild(div);
                div.scrollIntoView();
              }
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

          // Mensaje de bienvenida automático
          window.onload = function() {
            addMessage("¡Hola! Bienvenido al Chatbot de Informática. Pregúntame sobre evaluaciones o guías.", "bot");
          };

        </script>
      </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

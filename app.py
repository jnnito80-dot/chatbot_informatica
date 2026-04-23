from flask import Flask, request, jsonify
import json
import difflib

app = Flask(__name__)

with open("faq.json", "r", encoding="utf-8") as f:
    faq = json.load(f)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").lower()

    if user_message in faq:
        response = faq[user_message]
    else:
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
          body.light-theme {
            font-family: 'Segoe UI', sans-serif;
            margin:0; padding:0;
            background-color:#f5f5f5; /* Fondo claro */
            color:#000;
          }
          body.dark-theme {
            font-family: 'Segoe UI', sans-serif;
            margin:0; padding:0;
            background-color:#1e1e1e; /* Fondo oscuro */
            color:#e0e0e0;
          }

          #chatbox { 
            border:2px solid #4285f4; border-radius:10px;
            width:100%; height:100%;
            display:flex; flex-direction:column;
            background-color:inherit;
          }
          #header { 
            background:#333; color:white;
            padding:10px; display:flex;
            justify-content:space-between; align-items:center;
            font-weight:bold;
          }
          #messages { flex:1; padding:10px; overflow-y:auto; }
          .msg { margin:5px 0; padding:10px; border-radius:8px; max-width:80%; font-size:0.95em; }
          .user { background:#4285f4; color:#fff; align-self:flex-end; }
          .bot { background:#ffeb3b; color:#111; align-self:flex-start; } /* Texto oscuro sobre amarillo */
          #inputArea { display:flex; border-top:1px solid #555; }
          #inputArea input { flex:1; padding:10px; border:none; }
          #inputArea button { padding:10px; border:none; background:#4285f4; color:white; cursor:pointer; font-weight:bold; }
          #inputArea button:hover { background:#3064c9; }
          #themeToggle {
            background:none; border:none; cursor:pointer;
            font-size:1.2em; color:white;
          }
        </style>
      </head>
      <body class="dark-theme">
        <div id="chatbox">
          <div id="header">
            <span>🤖 Chatbot T56</span>
            <button id="themeToggle">🌙</button>
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
        
            // Dividir el texto en líneas
            const lines = text.split(/\\n/);
        
            // Convertir enlaces en clicables
            const formatLinks = (line) => line.replace(/(https?:\\/\\/\\S+)/g, '<a href="$1" target="_blank">$1</a>');
        
            let formatted = "";
        
            if (lines.length > 1) {
              // Crear lista con viñetas
              formatted = "<ul>";
              lines.forEach(line => {
                if (line.trim() !== "") {
                  formatted += "<li>" + formatLinks(line) + "</li>";
                }
              });
              formatted += "</ul>";
            } else {
              formatted = formatLinks(text);
            }
        
            // Si la respuesta es muy larga, ponerla en un cuadro con scroll y botón expandir/contraer con íconos
            if (text.length > 300 || lines.length > 5) {
              const container = document.createElement("div");
              container.style.maxHeight = "200px";
              container.style.overflowY = "auto";
              container.style.padding = "5px";
              container.style.border = "1px solid #ccc";
              container.style.borderRadius = "8px";
              container.style.background = "#fff";
              container.innerHTML = formatted;
        
              const toggleBtn = document.createElement("button");
              toggleBtn.innerHTML = "🔽"; // Ícono inicial (expandir)
              toggleBtn.style.marginTop = "5px";
              toggleBtn.style.padding = "5px 10px";
              toggleBtn.style.fontSize = "1em";
              toggleBtn.style.cursor = "pointer";
              toggleBtn.style.background = "#4285f4";
              toggleBtn.style.color = "#fff";
              toggleBtn.style.border = "none";
              toggleBtn.style.borderRadius = "5px";
        
              toggleBtn.onclick = function() {
                if (container.style.maxHeight === "200px") {
                  container.style.maxHeight = "none";
                  toggleBtn.innerHTML = "🔼"; // Ícono para contraer
                } else {
                  container.style.maxHeight = "200px";
                  toggleBtn.innerHTML = "🔽"; // Ícono para expandir
                }
              };
        
              div.appendChild(container);
              div.appendChild(toggleBtn);
            } else {
              div.innerHTML = formatted;
            }
        
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

          // Mensaje de bienvenida automático y aplicar tema guardado
          window.onload = function() {
            addMessage("¡Hola! Bienvenido al Chatbot de Informática. Pregúntame sobre evaluaciones o guías.", "bot");
            const savedTheme = localStorage.getItem("chatTheme");
            if (savedTheme) {
              document.body.className = savedTheme;
              document.getElementById("themeToggle").innerHTML = savedTheme === "dark-theme" ? "🌙" : "☀️";
            }
          };

          // Alternar tema y guardar preferencia
          document.getElementById("themeToggle").onclick = function() {
            const body = document.body;
            if (body.classList.contains("dark-theme")) {
              body.classList.remove("dark-theme");
              body.classList.add("light-theme");
              this.innerHTML = "☀️";
              localStorage.setItem("chatTheme", "light-theme");
            } else {
              body.classList.remove("light-theme");
              body.classList.add("dark-theme");
              this.innerHTML = "🌙";
              localStorage.setItem("chatTheme", "dark-theme");
            }
          };
        </script>
      </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

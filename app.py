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
          body { 
              font-family: 'Segoe UI', sans-serif; 
              margin:0; 
              padding:0; 
              background-color:#1e1e1e; /* Fondo oscuro */
              color:#e0e0e0; /* Texto claro */
            }
            
            #chatbox { 
              border:2px solid #4285f4; 
              border-radius:10px; 
              width:100%; 
              height:100%; 
              display:flex; 
              flex-direction:column; 
              background-color:#2c2c2c; /* Caja oscura */
            }
            
            #header { 
              background:#333; 
              color:#fff; 
              padding:10px; 
              display:flex; 
              justify-content:center; 
              align-items:center; 
              font-weight:bold;
            }
            
            #messages { 
              flex:1; 
              padding:10px; 
              overflow-y:auto; 
              background-color:#1e1e1e; /* Fondo oscuro */
            }
            
            .msg { 
              margin:5px 0; 
              padding:10px; 
              border-radius:8px; 
              max-width:80%; 
              font-size:0.95em; 
            }
            
            .user { 
              background:#4285f4; /* Azul brillante */
              color:#fff; 
              align-self:flex-end; 
            }
            
            .bot { 
              background:#ffeb3b; /* Amarillo vibrante */
              color:#000; 
              align-self:flex-start; 
            }
            
            #inputArea { 
              display:flex; 
              border-top:1px solid #555; 
              background-color:#2c2c2c; 
            }
            
            #inputArea input { 
              flex:1; 
              padding:10px; 
              border:none; 
              background-color:#1e1e1e; 
              color:#e0e0e0; 
            }
            
            #inputArea button { 
              padding:10px; 
              border:none; 
              background:#4285f4; 
              color:white; 
              cursor:pointer; 
              font-weight:bold; 
            }
            
            #inputArea button:hover { 
              background:#3064c9; 
            }

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
        
            // Dividir el texto en líneas
            const lines = text.split(/\n/);
        
            // Convertir enlaces en clicables
            const formatLinks = (line) => line.replace(/(https?:\/\/\S+)/g, '<a href="$1" target="_blank">$1</a>');
        
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

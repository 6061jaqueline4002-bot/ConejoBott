from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# -- Logica del bot -- #
def responder_usuario(mensaje):
    mensaje = mensaje.lower()
    if "hola" in mensaje:
        return "¡Hola! Soy ConejoBot 😊 ¿en qué puedo ayudarte hoy?"
    elif "adiós" in mensaje or "gracias" in mensaje:
        return "¡Hasta luego! Espero haberte ayudado 😊"
    else:
        return "No entiendo muy bien 😊, ¿podrías decirlo de otra forma?"

# -- Rutas -- #
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/enviar", methods=["POST"])
def enviar():
    data = request.get_json()
    mensaje_usuario = data.get("mensaje", "")  # ← Corregí esta línea
    respuesta = responder_usuario(mensaje_usuario)
    return jsonify({"respuesta": respuesta})

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)

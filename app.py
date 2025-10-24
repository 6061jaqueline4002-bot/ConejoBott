# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ======================================================
# INFORMACIÓN COMPLETA DEL CHATBOT CONEJOBOT_ITTG
# ======================================================

introduccion = """
¡Hola! Soy 🐰 ConejoBot_ITTG, tu asistente virtual del Instituto Tecnológico de Tuxtla Gutiérrez. 
Puedo darte información sobre los siguientes departamentos:
📘 Departamento de Inglés  
📗 Servicios Escolares  
📙 División de Estudios Profesionales  
📕 Coordinación

Solo escribe algo como:  
- “Información sobre el servicio social”  
- “Requisitos del TOEFL”  
- “Cómo tramito mi credencial”  
"""

# === Información completa (idéntica al código de consola) ===
indicaciones = {
    "Departamento de Inglés": {
        "cursos de inglés": """📘 **Cursos de Inglés**
            "1.-Percatarse de los flayers de convocatorias sobre los cursos\npublicadas en paginas oficiales del ITTG. Se indican 2 fechas que\ncorresponden al PRE-REGISTRO y REGISTRO(INSCRIPCIÓN).\n\n2.-Accesar al código QR de estos y llenar el formulario de pre-registro.\n\n3.-En este llenado seleccionar el horario de tu preferencia y el nivel al\nque ingresarás (importante realizar previamente el examen de ubicación).\n\n4.-Después de enviar el formulario, esperar el correo de confirmación\nde los grupos que seran abiertos.\n\n5.-En este correo se anexara un pdf con las indicaciones a seguir para\nhacer correctamente el procedimiento por medio de otro link (formulario).\n\n6.-Once hecho esto, dirígete a solicitar tu referencia bancaria al SII\ndesde la pestaña “ Documentos oficiales” seguido de “Solicitar”.\n\n7.-Seleccionas aquí tu nivel registrado en el formulario y presionas el\nbotón de generar referencia.\n\n8.-Con la información de tu referencia realiza el pago en la fecha limite\nestablecida en este.\n\n9.-Ingresar al link de REGISTRO Y posterior a esto envía tu comprobante\nde pago y la referencia antes generada.\n\n10.-Espera a ser contactado por tu docente para ser agregado correctamente\na las plataformas (no olvides poner todos tus datos correctamente).",.""",

        "examen de colocación": """📝 **Examen de colocación**
El examen de ubicación se realiza al inicio de cada semestre. 
            "2": "Para presentar el examen de ubicación, el estudiante deberá:\n1.- Estar atento a las convocatorias publicadas en las redes oficiales del TECNM.\n2.- Realizar el registro correspondiente.\n3.- Efectuar el pago indicado en la convocatoria.\nNota: La aplicación del examen de ubicación se realiza únicamente al inicio de cada semestre.""",

        "certificaciones": """🎓 **Certificaciones**
            "1.-Para solicitar la convalidación de un certificado de inglés, es necesario entregar:\n- Solicitud de liberación.\n- Número de control.\n- Nombre completo.\n- Periodo del último curso cursado.\n- Certificado de Inglés expedido por Institución validada por la SEP\n\nVigencia de los certificados:\n- TOEFL: 2 años.\n- Cambridge: 10 años.",  
📅 TOEFL tiene una vigencia de 2 años.  
📅 Cambridge tiene una vigencia de 10 años.""",

        "toefl": """📘 **TOEFL**
El examen TOEFL se aplica 4 veces al año.  
            "Los estudiantes interesados deberán:\n1.- Estar atentos a las convocatorias publicadas en las páginas oficiales del TECNM.\n2.- Haber cursado previamente los niveles correspondientes de inglés.\n3.- Realizar el registro y el pago correspondiente.\nNota: Se llevan a cabo cuatro aplicaciones del examen TOEFL al año""",

        "duración de los cursos": """⏰ **Duración de los cursos**
                        ""- Se imparten dos cursos por semestre, con una duración aproximada de 5 semanas por curso.\n- Cursos Superintensivos:Duración total de 120 horas por semestre, distribuidas en 4 cursos, con una duración aproximada de 12 semanas.",
-Cursos básicos e intermedios: 45 horas cada uno.  
- Cursos superintensivos: 120 horas por semestre.""",

        "contacto": """📞 **Contacto del Departamento de Inglés**
Teléfono: 961 615 0461 ext. 327  
Correo: leng_tgutierrez@tecnm.mx  
Ubicación: Edificio G"""
    },

    "Servicios Escolares": {
        "credencial": """🪪 **Credencial digital**
Ingresa a 👉 [http://credenciales.tuxtla.tecnm.mx/](http://credenciales.tuxtla.tecnm.mx/)  
Usa tu correo institucional y contraseña del mismo para generar tu credencial digital.
            .-Una vez dentro de la sesión verifica que tus datos personales y\nescolares sean correctos.\n\n4.-Da click al botón TOMAR FOTOGRAFÍA\na)Toma una fotografía al instante, la plataforma no permitirá cargar archivos desde tu galería de fotos.\nb)Debes utilizar camisa o playera blanca.\nc)El fondo de la fotografía debe ser de un color uniforme\n(puede ser color gris o colores claros), en una pared lisa sin logotipos.\nd)Procura que la iluminación sea la adecuada para que tu rostro pueda ser visible.\ne)La toma debe ser totalmente de frente, enfocando unicamente tu rostro\ny hombros (no tomar fotos de cuerpo completo).\nf)En el caso de utilizar lentes y/o piercings retirarlos para la fotografía.\ng)No usar gorras ni sombreros.\nh)MUJERES:cabello recogido o suelto sin tapar el rostro acompañado de un maquillaje discreto \ny aretes pequeños.\ni)HOMBRES:Sin barba, sin bigote, con la frente despejada\nsi tienes cabello largo deberás sujetarlo para mejor visibilidad del rostro.\nNota:Si la fotografía no cumple con los requisitos será RECHAZADA y\ndeberás tomarla nuevamente hasta que sea validada por el departamento de Servicios Escolares.\n\n5.-Ingresa tu firma, procura que sea idéntica a la de tu INE o alguna\nidentificación vigente).\n\n6.-Espera a la validación de tus datos por el Departamento de\nServicios Escolares.\n\n7.-Cuando tu info. sea validada se activará la opción GENERAR\nCREDENCIAL DIGITAL y SOLICITAR CREDENCIAL FÍSICA.",""",

        "constancia": """📄 **Constancia**
1️⃣ Genera la referencia bancaria en el SII.  
2️⃣ Realiza el pago.  
3️⃣ Envía el comprobante al correo ventanilla_escolares@tuxtla.tecnm.mx.""",

        "boleta": """📊 **Boleta oficial**
Solicita tu boleta al correo ventanilla_escolares@tuxtla.tecnm.mx.  
Tiempo estimado de entrega: 3 a 5 días hábiles.""",

        "kardex": """📑 **Kárdex**
Genera la referencia bancaria desde el SII y envía tu comprobante de pago al correo ventanilla_escolares@tuxtla.tecnm.mx.""",

        "acom": """🎓 **Actividades Complementarias (ACOM)**
Requieres 5 créditos totales. Puedes obtenerlos en:  
✅ Tutorías  
✅ Extraescolares  
✅ MOOC  
✅ Eventos académicos."""
    },

    "División de Estudios Profesionales": {
        "servicio social": """🛠 **Servicio Social**
El servicio social tiene una duración de 500 horas.  
Requisitos:  
- Tener 70% de créditos  
- Registrarte en el SII y elegir una dependencia aprobada  
- Entregar los reportes mensuales y finales.  
¿Quieres que te muestre los pasos completos del trámite?""",

        "residencias": """🏢 **Residencias Profesionales**
Consulta los requisitos en la División de Estudios Profesionales.  
Debes entregar: carta de presentación, plan de trabajo y reportes parciales.  
Duración: 640 horas."""
    },

    "Coordinación": {
        "traslado": """🚗 **Traslado**
Requiere solicitud formal, kárdex actualizado y comunicación entre la institución de origen y la receptora. 
Debe ser autorizado por la Dirección General del TecNM.""",

        "movilidad": """✈️ **Movilidad Estudiantil**
Consulta las convocatorias oficiales de movilidad nacional o internacional en la página del ITTG. 
Entrega tu solicitud con tu historial académico.""",

        "convalidación": """📚 **Convalidación**
Permite cambiar de plan de estudios o cursar una segunda carrera dentro del TecNM. 
Debes presentar tu historial académico y las materias cursadas.""",

        "equivalencia": """📘 **Equivalencia**
Permite equiparar estudios realizados en otras instituciones. 
Se requiere certificado parcial y programas de estudio validados."""
    }
}

# ======================================================
# FUNCIÓN PRINCIPAL DEL CHATBOT
# ======================================================
def responder_usuario(mensaje):
    mensaje = mensaje.lower()

    # Buscar coincidencias en todas las categorías
    for categoria, opciones in indicaciones.items():
        for clave, respuesta in opciones.items():
            if clave in mensaje:
                return respuesta

    # Respuestas generales
    if "hola" in mensaje:
        return introduccion
    elif "gracias" in mensaje or "adiós" in mensaje:
        return "🐰 ¡De nada! Espero haberte ayudado. ¡Nos vemos pronto!"
    elif "menu" in mensaje or "departamentos" in mensaje:
        return introduccion
    else:
        return "😅 No entiendo muy bien. Puedes escribir por ejemplo: 'información sobre servicio social', 'examen TOEFL' o 'cómo tramitar mi credencial'."

# ======================================================
# RUTAS DE FLASK
# ======================================================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/enviar", methods=["POST"])
def enviar():
    data = request.get_json()
    mensaje_usuario = data.get("mensaje", "")
    respuesta = responder_usuario(mensaje_usuario)
    return jsonify({"respuesta": respuesta})

# ======================================================
# EJECUCIÓN
# ======================================================
if __name__ == "__main__":
    app.run(debug=True)

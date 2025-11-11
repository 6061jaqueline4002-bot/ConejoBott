# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime
from database import (
    registrar_usuario,
    obtener_usuarios,
    guardar_calificacion,
    cargar_calificaciones,
    obtener_historial
)

DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)
CONTADOR_FILE = os.path.join(DATA_FOLDER, "contador_usuarios.txt")
REGISTRO_FILE = os.path.join(DATA_FOLDER, "registro_usuarios.txt")

def obtener_contador():
    #Carga el contador desde archivo de forma segura
    try:
        if os.path.exists(CONTADOR_FILE):
            with open(CONTADOR_FILE, "r", encoding='utf-8') as f:
                contenido = f.read().strip()
                if contenido and contenido.isdigit():
                    return int(contenido)
        return 0
    except Exception as e:
        print(f"❌ Error leyendo contador: {e}")
        return 0

def guardar_contador(valor):
    """Guarda el contador en archivo de forma segura"""
    try:
        with open(CONTADOR_FILE, "w", encoding='utf-8') as f:
            f.write(str(valor))
        # Forzar escritura inmediata
        os.fsync(f.fileno())
        print(f"✅ Contador guardado: {valor}")
    except Exception as e:
        print(f"❌ Error guardando contador: {e}")

def registrar_usuario():
    """Registra cada conexión en el historial"""
    global usuarios_activos
    try:
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(REGISTRO_FILE, "a", encoding='utf-8') as f:
            f.write(f"Usuario #{usuarios_activos} - Conexión: {ahora}\n")
        # Forzar escritura inmediata
        os.fsync(f.fileno())
        print(f"✅ Usuario registrado: #{usuarios_activos}")
    except Exception as e:
        print(f"❌ Error registrando usuario: {e}")

# Funciones para las calificaciones (prueba)
def cargar_calificaciones():
    """Carga las calificaciones desde el archivo JSON"""
    try:
        if os.path.exists(CALIFICACIONES_FILE):
            with open(CALIFICACIONES_FILE, "r", encoding='utf-8') as f:
                return json.load(f)
        # Estructura inicial si no existe el archivo
        return {
            "total_calificaciones": 0,
            "promedio": 0,
            "distribucion": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0},
            "calificaciones": []
        }
    except Exception as e:
        print(f"❌ Error cargando calificaciones: {e}")
        return {
            "total_calificaciones": 0,
            "promedio": 0,
            "distribucion": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0},
            "calificaciones": []
        }

def guardar_calificacion(estrellas, comentario=""):
    """Guarda una nueva calificación"""
    try:
        calificaciones = cargar_calificaciones()
        
        nueva_calificacion = {
            "estrellas": estrellas,
            "comentario": comentario,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "id": calificaciones["total_calificaciones"] + 1
        }
        
        # Actualizar estadísticas
        calificaciones["total_calificaciones"] += 1
        calificaciones["distribucion"][str(estrellas)] += 1
        calificaciones["calificaciones"].append(nueva_calificacion)
        
        # Calcular nuevo promedio
        total_puntos = sum(int(estrellas) * count for estrellas, count in calificaciones["distribucion"].items())
        calificaciones["promedio"] = round(total_puntos / calificaciones["total_calificaciones"], 1) if calificaciones["total_calificaciones"] > 0 else 0
        
        # Guardar en archivo
        with open(CALIFICACIONES_FILE, "w", encoding='utf-8') as f:
            json.dump(calificaciones, f, indent=2, ensure_ascii=False)
        os.fsync(f.fileno())
        
        print(f"✅ Calificación guardada: {estrellas} estrellas")
        return True
    except Exception as e:
        print(f"❌ Error guardando calificación: {e}")
        return False

# Contador global de usuarios - SE CARGA AL INICIAR
usuarios_activos = obtener_contador()
print(f"🚀 Servidor iniciado. Usuarios actuales: {usuarios_activos}")

app = Flask(__name__)
app.jinja_env.autoescape = False

# INFORMACIÓN COMPLETA DEL CHATBOT
introduccion = """
¡Hola! Soy 🐰 ConejoBot, tu asistente virtual del Instituto Tecnológico de Tuxtla Gutiérrez. 
Puedo darte información sobre los siguientes departamentos:
📘 Departamento de Inglés  
📗 Servicios Escolares  
📙 División de Estudios Profesionales  
📕 Coordinación Ing.Industrial

Solo escribe algo como:  
- “Información sobre el servicio social”  
- “Requisitos del TOEFL”  
- “Cómo tramito mi credencial”  
"""
# BASE DE CONOCIMIENTO ACTUALIZADA 

departamentos = {
    "Inglés": {
        "nombre": "📘 Departamento de Inglés",
        "keywords": ["inglés", "ingles", "curso", "toefl", "colocación", "certificación", "idiomas", "nivel", "duración", "examen"],
        "temas": {
            "Cursos de inglés": [
                "🔹Percatarse de los flayers de convocatorias sobre los cursos publicadas en páginas oficiales del ITTG. Se indican 2 fechas que corresponden al pre-registro y registro 'inscripción'.",
                "🔹Accesar al código QR de estos y llenar el formulario de pre-registro",
                "🔹En este llenado seleccionar el horario de tu preferencia y el nivel al que ingresarás.",
                "🔹Después de enviar el formulario, esperar el correo de confirmación de los grupos que serán abiertos.",
                "🔹En este correo se anexará un PDF con las indicaciones a seguir para hacer correctamente el procedimiento por medio de otro link (formulario).",
                "🔹Una vez hecho esto, dirígete a solicitar tu referencia bancaria al SII desde la pestaña “Documentos oficiales” seguido de “Solicitar”.",
                "🔹Seleccionas aquí tu nivel registrado en el formulario y presionas el botón de generar referencia.",
                "🔹Con la información de tu referencia realiza el pago en la fecha límite establecida en este.",
                "🔹Ingresar al enlace de REGISTRO Y posterior a esto envía tu comprobante de pago y la referencia antes generada en un solo archivo de PDF.",
                "🔹Espera a ser contactado por tu docente para ser agregado correctamente a las plataformas (no olvides poner todos tus datos correctamente)."
            ],
            "Examen de colocacion": [
                "Para presentar el examen de ubicación, el estudiante deberá:",
                "✅Estar atento a las convocatorias publicadas en las redes oficiales del TECNM.",
                "✅Realizar el registro correspondiente.",
                "✅Efectuar el pago indicado en la convocatoria. 💵💳",
                "Nota: La aplicación del examen de ubicación se realiza únicamente al inicio de cada semestre 🗓️."
            ],
            "Certificaciones de lengua extrajera": [
                "Para solicitar la convalidación de un certificado de inglés, es necesario entregar:",
                "✔️Solicitud de liberación.",
                "✔️Número de control.",
                "✔️Nombre completo.",
                "✔️Periodo del último curso cursado.",
                "✔️Certificado de Inglés expedido por Institución validada por la SEP",
                "📅 TOEFL tiene una vigencia de 2 años.  ",
                "📅 Cambridge tiene una vigencia de 10 años."
            ],
            "TOEFL": [
                "📅El examen TOEFL se aplica 4 veces al año.",
                "Los estudiantes interesados deberán:.",
                "1️⃣Estar atentos a las convocatorias publicadas en las páginas oficiales del TECNM.",
                "2️⃣Haber cursado previamente los niveles correspondientes de inglés.",
                "3️⃣Realizar el registro y el pago correspondiente."
            ],
            "Duración de cursos de inglés": [
                "⏳Cursos básicos e intermedios: 45 horas cada uno.",
                "⏳Cursos superintensivos: 120 horas por semestre."
            ],
            "Contactos del departamento de inglés": [
                "🏢Puedes acudir directamente al Departamento de Inglés del ITTG, Edificio G.",
                "📞Teléfono: 961 615 0461 ext. 327",
                "📧Correo de contacto: leng_tgutierrez@tecnm.mx "
            ]
        }
    },

    "Servicios escolares": {
        "nombre": "📗 Servicios Escolares",
        "keywords": ["servicios", "escolares", "credencial", "constancia", "boleta", "kardex", "liberación", "acom", "extraescolares"],
        "temas": {
            "Credencial digital": [
                "🔸Ingresa a 👉 http://credenciales.tuxtla.tecnm.mx/ ",
                "🔸Usa tu correo institucional para generar tu credencial digital.",
                "🔸Una vez dentro de la sesión verifica que tus datos personales y escolares sean correctos.",
                "🔸Da click al botón TOMAR FOTOGRAFÍA",
                "a) Toma una fotografía al instante, la plataforma no permitirá cargar archivos desde tu galería de fotos.",
                "b) Debes utilizar camisa o playera blanca.",
                "c) El fondo de la fotografía debe ser de un color uniforme (puede ser color gris o colores claros), en una pared lisa sin logotipos.",
                "d) Procura que la iluminación sea la adecuada para que tu rostro pueda ser visible.",
                "e) La toma debe ser totalmente de frente, enfocando únicamente tu rostro y hombros (no tomar fotos de cuerpo completo).",
                "f) En el caso de utilizar lentes y/o piercings retirarlos para la fotografía.",
                "g) No usar gorras ni sombreros.",
                "h) MUJERES: cabello recogido o suelto sin tapar el rostro acompañado de un maquillaje discreto y aretes pequeños.",
                "i)HOMBRES: Sin barba, sin bigote, con la frente despejada si tienes cabello largo deberás sujetarlo para mejor visibilidad del rostro.",
                "Nota: Si la fotografía no cumple con los requisitos será RECHAZADA y deberás tomarla nuevamente hasta que sea validada por el departamento de Servicios Escolares.",
                "🔸Ingresa tu firma, procura que sea idéntica a la de tu INE o alguna identificación vigente).",
                "🔸Espera a la validación de tus datos por el Departamento de Servicios Escolares.",
                "🔸Cuando tu info. sea validada se activará la opción GENERAR CREDENCIAL DIGITAL y SOLICITAR CREDENCIAL FÍSICA."
            ],
            "Constancia": [
                "1️⃣Generar referencia bancaria en la página del SII, en el apartado de documentos oficiales en la opción de Constancia de estudios.",
                "2️⃣Realizar el pago, se puede realizar de dos maneras, por medio de transferencia o en cajero automático de Santander..",
                "3️⃣Enviar el comprobante de pago junto al documento generado al correo de 👉 fichas@tuxtla.tecnm.mx ",
                "4️⃣Esperar el comprobante oficial de pago.",
                "5️⃣Enviar el comprobante oficial de pago correo:👉 ventanilla_escolares@tuxtla.tecnm.mx",
                "6️⃣Esperar de 3 a 5 días hábiles para obtener la constancia."
            ],
            "Boleta oficial": [
                "📧Solicita tu boleta al correo 👉 ventanilla_escolares@tuxtla.tecnm.mx solicitando tu boleta oficial con sello y firma de la institución.",
                "Tiempo estimado de entrega: 3 a 5 días hábiles."
            ],
            "Kardex": [
                "1️⃣Generar referencia bancaria en la página del SII, en el apartado de documentos oficiales, dar click en la opción solicitar.",
                "2️⃣Elegir la opción de “Impresión de Kardex.",
                "3️⃣Realizar el pago, se puede realizar de dos maneras, por medio de transferencia o en cajero automático de Santander.",
                "4️⃣Enviar el comprobante de pago junto al documento generado del SII al correo de 👉 fichas@tuxtla.tecnm.mx.",
                "5️⃣Esperar el comprobante oficial de pago.",
                "6️⃣Enviar el comprobante oficial de pago al correo:👉 ventanilla_escolares@tuxtla.tecnm.mx.",
                "7️⃣Esperar de 3 a 5 días hábiles para obtener el Kardex oficial."
            ],
            "Constancia de liberación de lengua extranjera": [
                "1️⃣Generar referencia bancaria en la página del SII, en el apartado de documentos oficiales, dar click en la opción solicitar.",
                "2️⃣Elegir la opción de “Constancia de liberación de lengua extranjera.",
                "3️⃣Realizar el pago, se puede realizar de dos maneras, por medio de transferencia o en cajero automático de Santander.",
                "4️⃣Enviar el comprobante de pago junto al documento generado del SII al correo de 👉 fichas@tuxtla.tecnm.mx.",
                "5️⃣Esperar el comprobante oficial de pago.",
                "6️⃣Enviar el comprobante oficial de pago al correo:👉 ventanilla_escolares@tuxtla.tecnm.mx.",
                "7️⃣Esperar de 3 a 5 días hábiles para obtener la constancia."
            ],
            "Actividades Complementarias (ACOM)": [
                "📚Las Actividades Complementarias (ACOM) es un requisito para titulación.",
                "1️⃣Para liberar las actividades complementarias (ACOM's) es necesario tener 5 créditos.",
                "2️⃣Tienes 3 créditos asegurados al cursar la materia Tutoría 1 y 2, y Extraescolares (OJO algunos créditos valen 0.5).",
                "3️⃣Para obtener los dos créditos restantes puedes participar en actividades referentes al Aniversario de la Carrera de Industrial.",
                "4️⃣Cursar 3 de 4 cursos MOOC 👉 ( https://mooc.tecnm.mx/portal/ )  y acreditar la actividad complementaria). ENVIAR al correo:👉 solicitud.extraescolares@tuxtla.tecnm.mx o acudir al Departamento de Extraescolares (Edificio O frente a la chanca de futbol rápido.",
                "5️⃣OTRO medio es: llenar la hoja de firmas (En Biblioteca del ITTG lo consiguen) por acudir a Eventos culturales, cívicos o deportivos más acreditar la actividad complementaria.",
                "6️⃣Otra forma es: si Cursan 2 MOOC (👉 https://mooc.tecnm.mx/portal/ ) y el diploma que reciben (si lo aprobaron), lo llevan a desarrollo académico (Edificio EaD, planta alta) para el ACOM 7.",
                "7️⃣Una vez que se reúne los 5 créditos, reportarán al Departamento de Servicios Escolares.",
                "NOTA:",
                "ACOM 3 - Congresos o eventos académicos - Máximos 2 créditos.",
                "ACOM 7- Cursos o talleres - Máximos 2 créditos."
            ]
        }
    },

    "División de estudios profesionales": {
        "nombre": "📙 División de Estudios Profesionales",
        "keywords": ["división", "division", "servicio social", "residencia", "residencias"],
        "temas": {
            "Servicio social": [
                "1️⃣Para comenzar el proceso identifica si el periodo de servicio comprenderá el periodo escolar de enero–junio o el de agosto-diciembre. Las fechas serán publicadas en las convocatorias expedidas por el departamento correspondiente.",
                "2️⃣Dirígete al SII e ingresa al apartado de “Servicio social”. Verifica si el sistema reconoce el porcentaje mínimo de créditos para comenzar el servicio (70%).",
                "3️⃣Si no cumples con este porcentaje debes esperar a cumplirlo llegado el 7mo semestre o cubrirlo mediante el adelanto de materias. Y en caso de que, si cumpla, el sistema te permitirá acceder a la descarga de formatos requeridos.",
                "4️⃣Una vez descargados los formatos (carta de presentación), procede a llenarlos con tus datos personales y envíalos al correo indicado.",
                "5️⃣Deberás esperar a la asignación de plazas al lugar u organismo de tu elección y posterior a ello será abierto tu expediente se servicio social, el cual debe ser cubierto (terminado) en un lapso de 6 meses como mínimo y no mayor a 2 años con un total de 500 hrs.",
                "6️⃣Una vez que el organismo reciba tu información, este elaborará una carta de aceptación, la cual deberá ser entregada al departamento de gestión tecnológica y vinculación en conjunto con el plan de trabajo.",
                "7️⃣Cuando el departamento reciba y acepte la información, podrás comenzar con el desarrollo de actividades y la elaboración de los reportes solicitados bimestralmente.",
                "8️⃣Cuando envíes las actividades y los reportes pertinentes al departamento de gestión tecnológica y vinculación, se te asignará una calificación correspondiente a la evaluación final del servicio, la cual se verá reflejada en el kardex.",
                "9️⃣Por último, el departamento de gestión tecnológica y vinculación expedirá una carta de liberación y constancia de calificación del servicio social.",
                "🔟Las constancias de calificaciones son enviadas al departamento de servicios escolares para que ellos coloquen la calificación final en el kardex (como se menciona en el paso 8).",
                "1️⃣1️⃣El proceso finalizará cuando recibas la carta de liberación del servicio social y a su vez visualices en tu kardex, la calificación obtenida en tu servicio social."
            ],
            "Residencia Profesional": [
                "1️⃣Antes de iniciar el trámite, asegúrate de cumplir con:",
                "✅Tener liberado el servicio social.",
                "✅Haber acreditado las 5 actividades complementarias (ACOM’s).",
                "✅Tener al menos el 80% de los créditos aprobados del plan de estudios.",
                "✅No contar con asignaturas en “curso especial”.",
                "2️⃣Elegir un proyecto de residencia, puede ser mediente los siguientes rubros:",
                "🏫Banco de proyectos del Instituto.",
                "🤓Propuesta propia, presentada por el estudiante.",
                "🏢Proyecto dentro de la empresa donde ya trabajas.",
                "Nota:La División de Estudios Profesionales, a través del coordinador de carrera, te asesora para que el proyecto sea adecuado a tu perfil profesional.",
                "3️⃣Desarrolla un anteproyecto de residencia profesional, donde definas:",
                "🔸Nombre del proyecto",
                "🔸Objetivos",
                "🔸Justificación",
                "🔸Actividades y cronograma",
                "🔸Lugar donde se realizará",
                "El asesor interno evalúa la viabilidad del anteproyecto.",
                "4️⃣Tramitar las cartas oficiales",
                "🔸Carta de presentación y agradecimiento, emitida por el Instituto y dirigida a la empresa u organismo.",
                "🔸La empresa deberá responder con una Carta de aceptación del residente.",
                "5️⃣Solicitud formal de residencia",
                "🔸Ingresa al portal de estudiantes 👉 https://estudiantes.tuxtla.tecnm.mx/ y llena la solicitud de residencia profesional.",
                "🔸Adjunta los documentos requeridos (anteproyecto, cartas, comprobantes, etc.).",
                "6️⃣Asignación de asesores",
                "🔸Asesor interno: profesor del Instituto que guía y evalúa tu proyecto.",
                "🔸Asesor externo: designado por la empresa o dependencia. Ambos supervisan el desarrollo y la solución de problemas del proyecto.",
                "7️⃣Reinscripción al Instituto",
                "✅Debes reinscribirte oficialmente durante el periodo correspondiente:",
                "🔸Solo a Residencia Profesional si es de tiempo completo.",
                "🔸O junto con materias adicionales, sin descuidar tu residencia.",
                "8️⃣Desarrollo del proyecto",
                "🔸Duración mínima de 4 meses y máxima de 6 meses, con un total de 500 horas acumuladas.",
                "🔸Cumple con el horario establecido por la empresa.",
                "🔸Mantén comunicación constante con ambos asesores.",
                "9️⃣Elaboración del informe final",
                "🔸Al concluir el proyecto, elabora el informe técnico con los resultados obtenidos.",
                "🔸Debe ser revisado y aprobado por los asesores interno y externo.",
                "🔟Se acredita mediante la realización del proyecto en alguno de los siguientes ámbitos",
                "🔸Sector social o productivo",
                "🔸Innovación y desarrollo tecnológico",
                "🔸Investigación",
                "🔸Diseño y/o construcción de equipo",
                "🔸Proyectos académicos autorizados",
                "🔸Educación dual o proyectos integradores",
                "💯Los asesores entregan las evaluaciones finales para acreditar la residencia (valor de 10 créditos)."
            ],
            "Titulación": [
                "1️⃣Para iniciar con el proceso de titulación es importante contar con la documentación correcta:",
                "✅Original y copia de solicitud de titulación",
                "✅Copia de certificado de licenciatura",
                "✅Copia de constancia de servicio social",
                "✅Copia de constancia de terminación de inglés ",
                "✅Entregar todos los documentos anteriores en una carpeta tamaño carta color beige.",
                "2️⃣Una vez que reúnas tus documentos, acude a entregarlos a la oficina de coordinación de apoyo a la titulación ubicada en el departamento de la división de estudios en el edificio A-B.",
                "3️⃣Es requisito obligatorio que para este punto cuentes con el inglés liberado, el servicio social concluido y con el certificado de terminación de estudios.",
                "4️⃣Posterior a la entrega de tus documentos, el departamento de coordinación de apoyo a la titulación solicitara la titulación al departamento correspondiente a tu carrera. ",
                "5️⃣Y este departamento posteriormente enviara tu información a la academia de tu carrera para que ellos se encarguen de evaluar el proyecto con el cual te titularas.",
                "6️⃣Luego de que la academia evalúe tu propuesta, te enviaran un documento vía correo institucional correspondiente a la aprobación de tu proyecto en conjunto del asesor que evaluara los avances de tu proyecto.",
                "7️⃣Si el proyecto de titulación será mediante la elaboración de una tesis, se te asignaran dos asesores y al finalizar tu proyecto deberás defenderla según la fecha y hora asignadas por el departamento de coordinación de apoyo a la titulación.",
                "8️⃣Una vez que el proyecto haya concluido y haya sido calificado o presentado, se expedirá un oficio de liberación de proyecto que deberá ser entregado al mismo departamento de apoyo a la titulación para que este otorgue un sello y finalice la parte académica del proceso.",
                "9️⃣La siguiente parte del proceso deberá finalizarse en el departamento de servicios escolares para llevar a cabo la parte administrativa bajo las indicaciones pertinentes de la o el encargado."
            ]            
        }
    },

    "Coordinación Ing.Industrial": {
        "nombre": "📕 Coordinación Ing.Industrial",
        "keywords": ["coordinacion", "coordinación", "traslado", "movilidad", "convalidación", "equivalencia"],        
        "temas": {
            "Traslado de instituto": [
                "1️⃣Antes de iniciar el trámite, identifica el periodo de reinscripción del Instituto receptor. El procedimiento debe comenzar previo a dichas fechas para garantizar la aceptación y registro oportuno.",
                "2️⃣Acude a la División de Estudios Profesionales del Instituto de origen y entrega:",
                "🔸Solicitud de Traslado (formato oficial, Anexo II), debidamente llenada y firmada.",
                "🔸Kárdex o constancia de calificaciones actualizada, que incluya: clave y nombre de todas las asignaturas cursadas, periodo en que se cursaron, calificación y oportunidad de acreditación.",
                "3️⃣La División de Estudios Profesionales del Instituto de origen:",
                "🔸Comprueba que el estudiante no tenga adeudos (material de laboratorio, libros, etc.).",
                "🔸Establece comunicación electrónica con la División de Estudios Profesionales del Instituto receptor para confirmar:",
                "a) Existencia del plan de estudios solicitado.",
                "b) Disponibilidad de asignaturas y capacidad.",
                "c) Fechas establecidas para el trámite.",
                "4️⃣Si el traslado es procedente:",
                "🔸La División de Estudios Profesionales del Instituto receptor emite el Oficio de Aceptación (Anexo III), con visto bueno del Departamento de Servicios Escolares del receptor, y lo envía electrónicamente (escaneado con firmas y sello).",
                "🔸Si el traslado no procede, se envía un correo electrónico notificando la improcedencia y el trámite concluye.",
                "5️⃣La División de Estudios Profesionales del Instituto de origen recibe el oficio de aceptación y lo turna al Departamento de Servicios Escolares del Instituto de origen para continuar el proceso.",
                "6️⃣El Departamento de Servicios Escolares del Instituto de origen:",
                "🔸Emite la Constancia de No Inconveniencia para Traslado (Anexo IV).",
                "🔸Prepara el kárdex o constancia de calificaciones actualizada.",
                "🔸Integra las constancias de actividades complementarias y servicio social acreditadas, cuando proceda.",
                "7️⃣El Departamento de Servicios Escolares del Instituto de origen envía al Departamento de Servicios Escolares del Instituto receptor, en sobre cerrado y sellado, únicamente:.",
                "🔸Kárdex o constancia de calificaciones actualizada.",
                "🔸Constancia de No Inconveniencia (Anexo IV).",
                "🔸Constancias de actividades complementarias y servicio social (si aplican).",
                "🔸El expediente completo se integra en el Instituto receptor al momento de la inscripción, solicitando al estudiante los documentos faltantes.",
                "8️⃣El trámite de inscripción puede iniciar con documentación electrónica; sin embargo, el Instituto de origen debe enviar los documentos originales al Instituto receptor en un plazo máximo de 20 días hábiles después del inicio de clases.",
                "9️⃣Una vez recibida la documentación original y registrada la carga académica: ",
                "🔸El estudiante queda adscrito al Instituto receptor.",
                "🔸Se conserva el historial académico, pero se pierden los beneficios particulares del Instituto de origen.",
                "🔸En traslados entre Institutos Descentralizados o de Descentralizado a Federal, se recomienda adecuar el número de control; entre Institutos Federales se conserva el mismo número."
            ],
            "Movilidad estudiantil": [
                "1️⃣Consulta las convocatorias oficiales de movilidad estudiantil publicadas por la División de Estudios Profesionales del Instituto de origen.",
                "Estas convocatorias indican:",
                "✅Calendario del programa.",
                "✅Requisitos académicos y administrativos..",
                "✅Fechas límite para entrega de documentos.",
                "2️⃣Antes de solicitar la movilidad, asegúrate de cumplir con:",
                "🔸No tener más de una asignatura en curso de repetición (salvo quienes participen en cursos de verano).",
                "🔸No tener adeudos de material, libros o equipo con el Instituto.",
                "🔸Que el periodo de movilidad no exceda tres semestres (consecutivos o alternos).",
                "🔸Cumplir con los requisitos específicos de la convocatoria.",
                "Entrega en la División de Estudios Profesionales del Instituto de origen:",
                "🔸Formato de Solicitud de Movilidad Estudiantil (Anexo IX).",
                "🔸Relación de asignaturas y programas correspondientes (si son de una IES extranjera, traducidos al español).",
                "🔸Información sobre la institución receptora y actividades académicas a realizar.",
                "4️⃣La División de Estudios Profesionales solicita al Departamento Académico y a la Academia realizar el análisis de compatibilidad de asignaturas.",
                "🔸Se elabora el Dictamen de Compatibilidad de Asignaturas.",
                "🔸Se turna copia al Departamento de Servicios Escolares para registro.",
                "5️⃣El Departamento de Servicios Escolares del Instituto de origen emite el Oficio de Solicitud de No Inconveniencia para Movilidad Estudiantil (Anexo XI) dirigido a la institución receptora, con base en el dictamen de compatibilidad.",
                "6️⃣La institución receptora envía el Oficio de No Inconveniencia para Movilidad Estudiantil o el documento equivalente que autoriza la participación del estudiante en el programa.",
                "7️⃣La División de Estudios Profesionales del Instituto receptor asigna la carga académica del estudiante en movilidad, conforme al documento recibido de la institución de origen. Si se trata de una IES extranjera, los documentos deben estar traducidos al español.",
                "8️⃣El estudiante cursa las asignaturas y actividades autorizadas en la institución receptora, manteniendo su inscripción vigente en el Instituto de origen.",
                "9️⃣Al concluir la movilidad:",
                "🔸La institución receptora envía el documento oficial que certifique la acreditación o no acreditación de las asignaturas y actividades realizadas (traducido al español si aplica).",
                "🔸El Departamento de Servicios Escolares del Instituto de origen registra los resultados en el historial académico del estudiante:",
                "🔸Si la movilidad fue en IES externas al TecNM, se asienta como AC (acreditada) o NA (no acreditada).",
                "🔸Si la movilidad fue dentro del TecNM, se asienta la calificación numérica obtenida."
            ],
            "Convalidación de materias": [
                "📌La convalidación está caracterizada por los siguientes aspectos:",
                "✅Permite al estudiante cambiar de un plan de estudio a otro dentro de las Instituciones adscritas al TecNM.",
                "✅Permite cursar una segunda carrera a nivel licenciatura, una vez que el egresado se ha titulado o ha aprobado su acto profesional de la primera carrera cursada.",
                "✅Permite al estudiante, que causó baja definitiva habiendo acreditado el 50% de créditos o más, reinscribirse en un plan de estudios diferente que le ofrezca el Instituto, con el propósito de que concluya una carrera profesional.",
                "📌Trámite para la convalidación de estudios:",
                "1️⃣El estudiante debe considerar que sólo tiene derecho a convalidar plan de estudios en una sola ocasión, bajo la condición que pueda concluir dicho plan de estudios dentro de los 12 semestres reglamentarios.",
                "2️⃣El interesado debe acudir a División de estudios profesionales del instituto de origen y entregar:",
                "🔸La solicitud de convalidación de estudios (formato oficial, anexo V) que lo puedes encontrar en página web👉 https://www.tuxtla.tecnm.mx/ en el apartado de estudiantes, en la opción de división de estudios y luego dar clic en movilidad estudiantil.",
                "🔸Documentos probatorios (kárdex o certificado parcial con calificaciones). Al menos 30 días hábiles antes de iniciar el siguiente semestre.",
                "3️⃣Sólo son convalidadas las asignaturas que se encuentren acreditadas.",
                "4️⃣Para realizar la convalidación en el plan de estudios al que se pretende cambiar y el que cursa actualmente, deben existir asignaturas comunes o similares, el contenido de los programas de estudio debe ser equiparable al menos en un 60 por ciento de las competencias específicas desarrolladas.",
                "5️⃣La División de Estudios Profesionales o su equivalente en los Institutos Tecnológicos Descentralizados, verifica los requisitos conforme al lineamiento.Si cumple, pasar al siguiente numeral; si no cumple, se le da a conocer al solicitante en el mismo formato de la solicitud.",
                "6️⃣La autorización de la convalidación de estudios queda condicionada con la capacidad del Instituto para el plan de estudios solicitado."
            ],
            "Equivalencia": [
                "📌Es el proceso mediante el cual se hacen equiparables entre sí los estudios realizados en Instituciones del Sistema Educativo Nacional diferentes a las Instituciones adscritas al TecNM.",
                "📄Requerimientos (documentos en original y copia)",
                "1️⃣Solicitud de Resolución de Equivalencia de estudios (Anexo XIII), que lo puedes encontrar en página web👉 https://www.tuxtla.tecnm.mx/ en el apartado de estudiantes, en la opción de división de estudios y luego dar clic en movilidad estudiantil.",
                "2️⃣Copia Certificada de acta de nacimiento (Los extranjeros, deberán presentar la documentación que acredite la calidad migratoria con que se encuentra en territorio nacional de acuerdo con la legislación aplicable).",
                "3️⃣Antecedentes académicos que acrediten que el interesado concluyó el nivel inmediato anterior a los estudios que se pretendan equiparar, es decir, certificado de nivel medio superior.",
                "4️⃣Certificado completo o incompleto de los estudios a equiparar.",
                "5️⃣Programas de estudios debidamente sellados por la Institución de procedencia.",
                "Comprobante de pago de dictamen técnico.",
                "7️⃣Comprobante de pago de derechos de la resolución de equivalencia."
            ]
        }
    }
}
def responder_usuario(mensaje):
    mensaje = mensaje.lower().strip()
    
    print(f"🔍 Mensaje recibido: '{mensaje}'")
    
    # PRIMERO: Buscar coincidencia EXACTA de temas
    for dep, datos in departamentos.items():
        for tema, info in datos["temas"].items():
            tema_lower = tema.lower()
            if tema_lower in mensaje:
                print(f"✅ Encontrado tema: {tema} en departamento: {dep}")
                texto = f"<b>{datos['nombre']}</b><br><br>"
                texto += f"<b>{tema}</b><br>"
                for item in info:
                    texto += f"• {item}<br>"
                return texto
    
    # SEGUNDO: Buscar por palabras clave ESPECÍFICAS
    palabras_clave_especificas = {
        "TOEFL": ["TOEFL", "examen toefl","toefl","examen toefl","certificado toefl","puntaje toefl","tofel","toef","toffel","toffle","toefel","toefle"],
        "Cursos de inglés": ["inscribirme a los cursos","Cursos de inglés","curso","inscribirme","niveles","clases de inglés","clases de ingles","curso de inglés", "cursos de inglés", "clases de inglés","clases inglés","aprender inglés","inglés básico","inglés intermedio","inglés avanzado","información sobre los cursos de inglés","A1","B1","A2","B1.1"],
        "Examen de colocación": ["examen de colocación", "colocacion", "ubicación","prueba colocación","colocación inglés","nivelación inglés","colocasion","examen","exámen","examén"],
        "Certificaciones de lengua extrajera": ["certificarme","certificar","CERTIFICAR","certificación", "certificaciones", "convalidación de inglés","certificado","acreditación","reconocimiento oficial"],
        "Credencial digital": ["credencial", "credencial digital", "credenciales","credencial electrónica","identificación digital"],
        "Servicio social": ["servicio social", "servicios social","horas servicio social","liberación servicio social"],
        "Constancia": ["constancia", "constancia de estudios","comprobante","documento oficial"],
        "Kardex": ["kardex", "historial académico","récord académico","boleta general","kárdex","Kárdex","Kardex",],
        "Residencias": ["residencias", "residencia","residencia profesional","práctica profesional"],
        "Movilidad estudiantil": ["movilidad", "movilidad estudiantil","intercambio"],
        "Traslado de instituto": ["traslado", "cambio de escuela","Cambio escuela","transferencia","cambiar de plantel","cambiar de tec","cambiar"],
        "Contactos del departamento de inglés": ["contacto de inglés", "comunicar","número","numero","información de los cursos","comunicarse","hablar con alguien","contacto"],
        "Boleta oficial": ["Tramitar boleta", "boleta oficial","boleta de estudio","calificaciones oficiales","boleta de calificaciones","boleta"],
        "Constancia de liberación de lengua extrajera": ["constancia de liberacion", "liberación de ingles","liberación lengua extranjera","constancia inglés","certificado inglés","liberar inglés"],
        "Actividades Complementarias (ACOM)": ["ACOM", "ACOM'S","acom","actividad complementaria","horas complementarias","actividades extracurriculares"],
        "Equivalencia": ["equivalencia","revalidación","convalidación","equivalencia de estudios"],
        "Residencia Profesional": ["Residencia","residencia profecional","tramite de residencia","práctica profesional","estadía profesional","residencia","residencias"],
        "Titulación": ["titulacion","titulación","Titulación","egreso","titulo","Titulo","título","titularme"],
        "Convalidación de materias": ["cambio de carrera","Cambio de carrera","convalidación","convalidación de materias","convalidacion","revalidación materias","equivalencia materias","convalidar materias","convalidar"],
        "Duración de cursos de inglés": ["duración de inglés", "tiempo","duración","duración de cursos de inglés","tiempo de los cursos","cuánto dura","horas curso"]
    }
    
    for tema_especifico, palabras in palabras_clave_especificas.items():
        if any(palabra in mensaje for palabra in palabras):
            print(f"✅ Encontrado por palabra clave: {tema_especifico}")
            for dep, datos in departamentos.items():
                for tema, info in datos["temas"].items():
                    if tema.lower() == tema_especifico.lower():
                        texto = f"<b>{datos['nombre']}</b><br><br>"
                        texto += f"<b>{tema}</b><br>"
                        for item in info:
                            texto += f"• {item}<br>"
                        return texto
    
    # TERCERO: Búsqueda directa por departamento
    if "coordinación" in mensaje or "coordinación" in mensaje:
        datos = departamentos["Coordinación Ing.Industrial"]
        texto = f"<b>{datos['nombre']}</b><br><br>"
        texto += "Tengo información sobre estos temas:<br><br>"
        for tema in datos["temas"].keys():
            texto += f"• <b>{tema}</b><br>"
        texto += f"<br>Escribe el <b>tema específico</b> que te interesa."
        return texto
        
    elif "Inglés" in mensaje or "inglés" in mensaje:
        datos = departamentos["Inglés"]
        texto = f"<b>{datos['nombre']}</b><br><br>"
        texto += "Tengo información sobre estos temas:<br><br>"
        for tema in datos["temas"].keys():
            texto += f"• <b>{tema}</b><br>"
        texto += f"<br>Escribe el <b>tema específico</b> que te interesa."
        return texto
        
    elif "Servicios escolares" in mensaje or "escolares" in mensaje:
        datos = departamentos["Servicios escolares"]
        texto = f"<b>{datos['nombre']}</b><br><br>"
        texto += "Tengo información sobre estos temas:<br><br>"
        for tema in datos["temas"].keys():
            texto += f"• <b>{tema}</b><br>"
        texto += f"<br>Escribe el <b>tema específico</b> que te interesa."
        return texto
        
    elif "División de estudios" in mensaje or "estudios profesionales" in mensaje:
        datos = departamentos["División de estudios profesionales"]
        texto = f"<b>{datos['nombre']}</b><br><br>"
        texto += "Tengo información sobre estos temas:<br><br>"
        for tema in datos["temas"].keys():
            texto += f"• <b>{tema}</b><br>"
        texto += f"<br>Escribe el <b>tema específico</b> que te interesa."
        return texto
    # CUARTO: Respuesta por defecto
    return (
        "¡Hola! Soy ConejoBot 🐰<br><br>"
        "Puedo ayudarte con información específica sobre:<br><br>"
        "📘 <b>Inglés:</b> cursos, examen TOEFL, certificaciones, examen de colocación<br>"
        "📗 <b>Servicios escolares:</b> credencial digital, constancias, boletas, kardex<br>"
        "📙 <b>División de estudios:</b> servicio social, residencias<br>"
        "📕 <b>Coordinación Ing.Industrial:</b> traslados, movilidad estudiantil, convalidación<br><br>"
        "💡 <i>Ejemplos: 'cursos de inglés', 'credencial digital', 'servicio social'</i>"
    )
#  RUTAS FLASK 
@app.route("/")
def home():
    registrar_usuario()  # registra conexión de usuario
    return render_template("index.html")

@app.route("/enviar", methods=["POST"])
def enviar():
    data = request.get_json()
    mensaje_usuario = data.get("mensaje", "")
    respuesta = responder_usuario(mensaje_usuario)
    return jsonify({"respuesta": respuesta})

@app.route("/calificar", methods=["POST"])
def calificar():
    data = request.get_json()
    estrellas = int(data.get("estrellas", 0))
    comentario = data.get("comentario", "")
    if estrellas < 1 or estrellas > 5:
        return jsonify({"message": "Calificación no válida"}), 400

    guardar_calificacion(estrellas, comentario)
    return jsonify({"message": "¡Gracias por tu calificación! ❤️"})


@app.route("/admin/estadisticas")
def admin_estadisticas():
    usuarios = obtener_usuarios()
    historial = obtener_historial()
    calif_data = cargar_calificaciones()

    return render_template(
        "admin_estadisticas.html",
        usuarios=usuarios,
        historial=historial,
        promedio=calif_data["promedio"],
        total_calificaciones=calif_data["total_calificaciones"],
        distribucion=calif_data["distribucion"],
        calificaciones=calif_data["calificaciones"],
        fecha=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    )

# EJECUCIÓN
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)


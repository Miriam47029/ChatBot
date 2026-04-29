import math
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ==========================================
# PRECIOS EN USD (AHORA SON POR DÍA)
# ==========================================
# Modifiqué los precios para que sean razonables por día
precios_destinos_usd_por_dia = {
    "cancun": 50, "paris": 170, "tokyo": 210, "madrid": 135,
    "nueva york": 115, "alemania": 130, "italia": 150, "londres": 180,
    "canada": 100, "colombia": 60, "europa": 150, "españa": 130,
    "corea": 160, "japon": 200, "argentina": 70, "brasil": 80,
    "peru": 50, "chile": 65, "costa rica": 45, "china": 140,
    "australia": 190, "miami": 90, "los angeles": 100
}

TARIFA_ESTANDAR_USD_POR_DIA = 100 
TIPO_DE_CAMBIO = 17.38

@app.route('/', methods=['GET','POST'])
def home():
    return render_template('index.html') 

@app.route('/cotizar', methods=['POST'])
def cotizar_viaje():
    datos = request.get_json()
    
    destino_usuario = datos.get('destino', '').lower().strip()
    dias = datos.get('dias', 7) 
    
    palabras_a_ignorar = ["quiero", "ir", "a", "viajar", "conocer", "el", "la", "los", "las", "tu destino"]
    for palabra in palabras_a_ignorar:
        destino_usuario = destino_usuario.replace(f" {palabra} ", " ").replace(f"^{palabra} ", "")
    
    destino_usuario = destino_usuario.strip()
    
    costo_usd_por_dia = None
    nombre_destino = ""

    for destino, precio in precios_destinos_usd_por_dia.items():
        if destino in destino_usuario:
            costo_usd_por_dia = precio
            nombre_destino = destino.title()
            break

    if not costo_usd_por_dia and len(destino_usuario) > 2:
        costo_usd_por_dia = TARIFA_ESTANDAR_USD_POR_DIA
        nombre_destino = destino_usuario.split()[-1].title()

    if costo_usd_por_dia:
        # LA NUEVA MATEMÁTICA: (Precio por día * Días) * 17.38
        costo_total_usd = costo_usd_por_dia * dias
        costo_mxn = costo_total_usd * TIPO_DE_CAMBIO
        
        texto_respuesta = (f"El costo para <b>{nombre_destino}</b> por {dias} días es de "
                           f"<b>${costo_mxn:,.2f} MXN</b>.<br>"
                           f"<span style='font-size:12px; color:#888;'>(Precio: ${costo_total_usd} USD)</span>")
        return jsonify({'mensaje': texto_respuesta})
    
    else:
        texto_error = ("No logré reconocer el destino. 🌍<br><br>"
                       "Asegúrate de escribir solo el nombre del lugar, por ejemplo: <b>Japón, Colombia o París</b>.")
        return jsonify({'mensaje': texto_error})

if __name__ == '__main__':
    app.run(debug=True)
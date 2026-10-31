"""
Generador de Documentacion Sintetica para Pruebas de Damm KnowledgeOps
Este script genera manuales tecnicos completamente ficticios y simulados
para validar el pipeline RAG sin utilizar ningun documento real ni confidencial.
"""

import os

SYNTHETIC_DATASET = {
    "sop_envasadora_krones_simulada.txt": """MANUAL DE OPERACION INDUSTRIAL - SIMULACION EDUCATIVA
Equipo: Envasadora Rotativa Krones Mod-Sim-2026
Departamento: Envasado y Embotellado
Version: 1.0 (Datos Sinteticos)

1. PROCEDIMIENTO DE PARADA DE EMERGENCIA:
En caso de detectar vibraciones anomalas, fuga de liquido o peligro inminente:
1.1. Presionar inmediatamente la seta roja de parada de emergencia ubicada en el panel frontal P-01 o en la estrella de entrada.
1.2. El sistema cortara la alimentacion neumatica de forma automatica reduciendo la presion a 0.0 bar.
1.3. Verificar que el carrusel de llenado se detenga por completo antes de abrir las compuertas de proteccion de metacrilato.
1.4. Notificar al supervisor de turno mediante el codigo de parada E-402.

2. CALIBRACION DE CABEZALES DE LLENADO:
2.1. Antes de iniciar el ajuste, verificar que la temperatura del cabezal sea inferior a 35 grados Celsius.
2.2. Ajustar el sensor micrometrico con la llave hexagonal de 4mm girando en sentido horario para aumentar 0.5mm el nivel de llenado.
2.3. Ejecutar ciclo de prueba en seco con 10 botellas testigo. Tolerancia permitida: +/- 1.5 ml.

3. ADVERTENCIAS DE SEGURIDAD CRITICA:
[PELIGRO CRITICO] Prohibido manipular los inyectores sin activar previamente el protocolo de consignacion electrica y neumatica LOTO (Lockout/Tagout). Riesgo de atrapamiento y proyeccion de presion residual.
""",

    "protocolo_loto_seguridad_simulado.txt": """PROTOCOLO GENERAL DE SEGURIDAD Y CONSIGNACION LOTO
Modulo: Seguridad Operacional de Planta
Version: 2.1 (Simulacion MetròpolisFPLab)

1. PRINCIPIOS DE BLOQUEO LOTO:
Toda intervencion mecanica o electrica superior a 15 minutos requiere consignacion estricta:
1.1. Aislar el disyuntor principal del cuadro electrico sectorial correspondiente.
1.2. Colocar el candado de seguridad personal rojo y la tarjeta de peligro identificada con el nombre del operario.
1.3. Purgar las lineas de aire comprimido secundario mediante la valvula de despresurizacion manual V-09.
1.4. Comprobar la ausencia de presion residual en el manometro analogo (debe marcar exactamente 0.0 bar).
1.5. Probar el arranque local de la maquina; la maquinaria no debe realizar ningun movimiento.

2. RETIRADA DE CONSIGNACION:
Solo el operario que coloco el candado tiene autorizacion para retirarlo tras verificar que las compuertas estan cerradas y el personal despejado.
""",

    "procedimiento_limpieza_cip_simulado.txt": """PROCEDIMIENTO OPERATIVO ESTANDAR - LIMPIEZA CIP (CLEAN-IN-PLACE)
Sistema: Circuito de Limpieza Quimica de Tanques
Version: 1.2 (Ficticio para pruebas)

1. FASES DEL CICLO CIP:
1.1. Pre-enjuague con agua osmotizada a 50 grados Celsius durante 10 minutos.
1.2. Lavado caustico con solucion de sosa al 2.0% a 75 grados Celsius durante 20 minutos para disolver restos organicos.
1.3. Enjuague intermedio con agua declorada.
1.4. Desinfeccion con solucion peracetica al 0.5% a temperatura ambiente (15 minutos).
1.5. Enjuague final y control de pH en retorno (el pH debe situarse entre 6.8 y 7.2 antes de autorizar el siguiente lote).

2. CONDICIONES DE SEGURIDAD QUIMICA:
[PELIGRO CRITICO] Obligatorio el uso de gafas de proteccion estancas, guantes de nitrilo de cana larga y pantalla facial. En caso de contacto accidental, lavar con agua abundante en la ducha de emergencia durante 15 minutos.
"""
}

def generate_docs(target_dir: str = "synthetic_dataset"):
    os.makedirs(target_dir, exist_ok=True)
    for filename, content in SYNTHETIC_DATASET.items():
        filepath = os.path.join(target_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        print(f"Generated synthetic doc: {filepath}")

if __name__ == "__main__":
    generate_docs()

import cv2
import requests
import os
import sys
from ultralytics import YOLO

# --- CONFIGURACIÓN ---
# En GitHub, el video debe estar subido en el repositorio junto al código
NOMBRE_VIDEO = "150505-798856143_small.mp4"
INTERVALO_SEGUNDOS = 2

# LEER CLAVES SECRETAS DE GITHUB
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# Si no hay claves, paramos para evitar errores
if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
    print("❌ Error: No se encontraron las credenciales de Telegram en las variables de entorno.")
    sys.exit(1)

ANIMALES_PELIGROSOS = ['bear', 'elephant', 'zebra', 'giraffe', 'bird']


def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje}
    try:
        requests.post(url, json=payload)
        print(f"✅ Notificación enviada: {mensaje}")
    except Exception as e:
        print(f"❌ Error enviando a Telegram: {e}")


def analizar_video():
    print(f"Iniciando análisis de {NOMBRE_VIDEO}...")

    # Cargar modelo
    model = YOLO('yolov8n.pt')
    cap = cv2.VideoCapture(NOMBRE_VIDEO)

    if not cap.isOpened():
        print(f"❌ No se pudo abrir el video. Asegúrate de que esté en el repo.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    frames_salto = int(fps * INTERVALO_SEGUNDOS)
    count = 0
    alerta_enviada = False  # Para no spammear en la misma ejecución

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if count % frames_salto == 0:
            results = model(frame, verbose=False)

            for box in results[0].boxes:
                cls_id = int(box.cls[0])
                animal = model.names[cls_id]
                confianza = float(box.conf[0]) * 100

                if animal in ANIMALES_PELIGROSOS and confianza > 40:
                    print(
                        f"⚠️ DETECTADO: {animal} ({confianza:.1f}%) en frame {count}")

                    # En GitHub Actions, como el script corre una vez y muere,
                    # enviamos 1 alerta y podemos salir o seguir buscando.
                    if not alerta_enviada:
                        msg = f"🚨 ALERTA AUTOMÁTICA GITHUB 🚨\nSe detectó: {animal} ({confianza:.1f}%)"
                        enviar_telegram(msg)
                        alerta_enviada = True
                        # Opcional: break (si solo quieres la primera alerta y terminar)

        count += 1

    cap.release()
    print("Análisis finalizado.")


if __name__ == "__main__":
    analizar_video()

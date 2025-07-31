import cv2
import time
from CR3LIVE import *
from control import move_up, move_down, prender_cinta2, prender_cinta3, apagar_cinta2, apagar_cinta3
from collections import deque
DELAY_SEGUNDOS = 0.8  # Tiempo desde detección hasta acción

def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara.")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    roi_width = int(frame_width * 0.2)
    roi_height = int(frame_height * 0.2)
    roi_x = (frame_width - roi_width) // 2
    roi_y = (frame_height - roi_height) // 2

    posicion_actual = "abajo"
    detecciones = deque()
    ultimo_color_detectado = None  # Para evitar repeticiones

    prender_cinta2()
    prender_cinta3()

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error al capturar el frame.")
                break

            cropped_frame = frame[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]
            if cropped_frame.size == 0:
                continue

            color = get_predominant_color_from_frame(cropped_frame)
            now = time.time()

            # Solo agregamos si cambió el color respecto al anterior
            if color != ultimo_color_detectado:
                detecciones.append((now, color))
                ultimo_color_detectado = color  # Actualizar el último

            # Verificamos si ya pasó el tiempo
            if detecciones and (now - detecciones[0][0]) >= DELAY_SEGUNDOS:
                _, color_procesar = detecciones.popleft()
                print(f"Ejecutando acción para color: {color_procesar}")

                if color_procesar == "red" and posicion_actual == "abajo":
                    move_up()
                    posicion_actual = "arriba"
                elif color_procesar not in ["red","gray" "unknown", "white (background)", "unknown (low confidence)"] and posicion_actual == "arriba":
                    move_down()
                    posicion_actual = "abajo"

            # Mostrar en pantalla
            cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_width, roi_y + roi_height), (0, 255, 0), 2)
            cv2.putText(frame, f"Detectado: {color.upper()}", (roi_x, roi_y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow("Video con ROI", frame)
            cv2.imshow("ROI Analizado", cropped_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cap.release()
        apagar_cinta2()
        time.sleep(0.5)
        apagar_cinta3()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

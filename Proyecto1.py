import cv2
import mediapipe as mp
import math

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Variables del objeto
grabbed = False
obj_x, obj_y = 300, 200
obj_size = 100
offset_x, offset_y = 0, 0

# Cargar imagen del objeto
obj_img = cv2.imread("objeto.png", cv2.IMREAD_UNCHANGED)
if obj_img is None:
    print("❌ ERROR: No se pudo cargar 'objeto.png'.")
    exit()
obj_img = cv2.resize(obj_img, (obj_size, obj_size))

# Función segura para superponer imagen con canal alfa
def overlay_image_alpha(img, img_overlay, x, y):
    h, w = img_overlay.shape[:2]
    ih, iw = img.shape[:2]

    # Ajuste si x o y son negativos
    if x < 0:
        img_overlay = img_overlay[:, -x:]
        w = img_overlay.shape[1]
        x = 0
    if y < 0:
        img_overlay = img_overlay[-y:, :]
        h = img_overlay.shape[0]
        y = 0

    # Cortar si se sale del borde
    if x + w > iw:
        w = iw - x
        img_overlay = img_overlay[:, :w]
    if y + h > ih:
        h = ih - y
        img_overlay = img_overlay[:h, :]

    if w <= 0 or h <= 0:
        return img

    overlay_rgb = img_overlay[..., :3]
    alpha = img_overlay[..., 3:] / 255.0

    img[y:y+h, x:x+w] = (1.0 - alpha) * img[y:y+h, x:x+w] + alpha * overlay_rgb
    return img

# Calcular distancia entre dos puntos
def distancia(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

# Iniciar cámara
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        print("❌ ERROR: No se pudo leer la cámara.")
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

            lm_list = []
            for lm in handLms.landmark:
                h, w, _ = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((cx, cy))

            if len(lm_list) >= 9:
                thumb_tip = lm_list[4]
                index_tip = lm_list[8]
                d = distancia(thumb_tip, index_tip)

                if d < 40:
                    if not grabbed:
                        grabbed = True
                        offset_x = index_tip[0] - obj_x
                        offset_y = index_tip[1] - obj_y
                    obj_x = index_tip[0] - offset_x
                    obj_y = index_tip[1] - offset_y
                else:
                    grabbed = False

    # Asegurar que no se salga del frame
    obj_x = max(0, obj_x)
    obj_y = max(0, obj_y)

    # Superponer la imagen del objeto
    frame = overlay_image_alpha(frame, obj_img, obj_x, obj_y)

    # Mostrar ventana
    cv2.imshow("Drag & Drop con Gestos", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()

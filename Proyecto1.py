import cv2
import mediapipe as mp
import math

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Variables de los objetos
obj_size = 100
grabbed_obj = None

# Cargar imágenes de los objetos
def cargar_objeto(path, x, y):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"❌ ERROR: No se pudo cargar '{path}'.")
        exit()
    img = cv2.resize(img, (obj_size, obj_size))
    return {
        "img": img,
        "x": x,
        "y": y,
        "grabbed": False,
        "offset_x": 0,
        "offset_y": 0
    }

obj1 = cargar_objeto("objeto.png", 100, 150)
obj2 = cargar_objeto("objeto1.png", 400, 250)
objetos = [obj1, obj2]

# Función para superponer imagen con canal alfa
def overlay_image_alpha(img, img_overlay, x, y):
    h, w = img_overlay.shape[:2]
    ih, iw = img.shape[:2]

    if x < 0:
        img_overlay = img_overlay[:, -x:]
        w = img_overlay.shape[1]
        x = 0
    if y < 0:
        img_overlay = img_overlay[-y:, :]
        h = img_overlay.shape[0]
        y = 0
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
                    if grabbed_obj is None:
                        # Intentar agarrar uno de los objetos
                        for obj in objetos:
                            dentro = obj["x"] <= index_tip[0] <= obj["x"] + obj_size and obj["y"] <= index_tip[1] <= obj["y"] + obj_size
                            if dentro:
                                grabbed_obj = obj
                                obj["grabbed"] = True
                                obj["offset_x"] = index_tip[0] - obj["x"]
                                obj["offset_y"] = index_tip[1] - obj["y"]
                                break
                    if grabbed_obj:
                        grabbed_obj["x"] = index_tip[0] - grabbed_obj["offset_x"]
                        grabbed_obj["y"] = index_tip[1] - grabbed_obj["offset_y"]
                else:
                    if grabbed_obj:
                        grabbed_obj["grabbed"] = False
                        grabbed_obj = None

    # Dibujar los objetos
    for obj in objetos:
        obj["x"] = max(0, obj["x"])
        obj["y"] = max(0, obj["y"])
        frame = overlay_image_alpha(frame, obj["img"], obj["x"], obj["y"])

    # Mostrar ventana
    cv2.imshow("Drag & Drop con 2 Objetos", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()

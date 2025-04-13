# miniProyecto1
Arrastrar y Soltar Virtual usando el Seguimiento de Manos en Python

🖐️ Proyecto Drag & Drop con Gestos usando OpenCV + MediaPipe
Este proyecto permite interactuar con objetos en pantalla utilizando gestos de la mano detectados por la cámara. Fue desarrollado con Python, y hace uso de MediaPipe para el seguimiento de la mano y OpenCV para el procesamiento de imagen. Los usuarios pueden "agarrar" y mover objetos virtuales como imágenes simplemente juntando los dedos índice y pulgar.

🎯 Objetivo
Crear una interfaz accesible para personas, ideal como ejemplo de interacción natural entre humanos y computadoras. El sistema permite:

Detectar gestos de la mano.

Agarrar y mover objetos arrastrables en pantalla.

Personalizar los objetos (por ejemplo, el logo de una universidad).

Funciona en tiempo real con una cámara web.

🖼️ Ejemplo visual
En este caso se usó el logo de la Universidad Mariano Gálvez como uno de los objetos que se pueden mover en pantalla:


📁 Estructura del Proyecto
bash
Copiar
Editar
📁 proyecto_drag_drop/
│
├── main.py                # Código principal del proyecto
├── objeto.png             # Imagen 1 (objeto arrastrable: logo UMG)
├── objeto1.png            # Imagen 2 (otro objeto arrastrable)
└── README.md              # Este archivo
✅ Requisitos
Instalá los siguientes paquetes de Python antes de ejecutar el proyecto:

bash
Copiar
Editar
pip install opencv-python mediapipe numpy
Si no usás entorno virtual, podés usar:

bash
Copiar
Editar
python -m pip install --upgrade pip
pip install -r requirements.txt
Nota: Si necesitás usar TensorFlow u otros modelos IA más adelante, también podés agregar:

bash
Copiar
Editar
pip install tensorflow
🧠 ¿Cómo Funciona?
MediaPipe Hands detecta la mano y sus puntos clave en tiempo real.

El programa calcula la distancia entre el dedo pulgar e índice.

Si están lo suficientemente cerca (ej. < 40 px), se considera un gesto de "agarre".

El objeto se mueve junto con la mano mientras ese gesto se mantiene.

Cuando se sueltan los dedos, el objeto queda en la nueva posición.

📦 Uso de Imágenes Personalizadas
Podés cambiar los objetos arrastrables simplemente reemplazando las imágenes:

U.png: Reemplazala con cualquier otro objeto que quieras mover.

Asegurate que las imágenes tengan transparencia (canal alfa) para que se vean bien (formato .png con fondo transparente).

▶️ Cómo Ejecutar
Colocá las imágenes dentro del mismo directorio del script.

Asegurate que tu cámara esté conectada.

Ejecutá el script:

bash
Copiar
Editar
python main.py
Mostrá la mano frente a la cámara, juntá índice y pulgar sobre el objeto… ¡y arrastralo!

📌 Consejos
Asegurate de tener buena iluminación para que la cámara y MediaPipe detecten bien la mano.

Podés ajustar la distancia mínima de agarre (d < 40) si necesitás más o menos precisión.

Las imágenes deben tener dimensiones apropiadas (100x100, 150x150, etc.).

🚀 Ideas Futuras
Detectar múltiples manos.

Añadir sonido al agarrar o soltar objetos.

Exportar este sistema para usarlo como interfaz en una app móvil.

Integrar con text-to-speech para personas con discapacidad visual.

📍 Créditos
Desarrollado con ❤ usando Python, OpenCV y MediaPipe.

Imagen del logo: Universidad Mariano Gálvez de Guatemala.

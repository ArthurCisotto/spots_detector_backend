import os
from ultralytics import YOLO
import cv2
import numpy as np
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings
import base64


def process_image_with_yolo(image_file):
    #print current working directory
    
    model_path = os.path.join(settings.MODEL_ROOT, 'runs', 'detect', 'train11', 'weights', 'best.pt')
    #model_path = 'backend/spots_detector/backend/yolo_model/runs/detect/train6/weights/best.pt'
    model = YOLO(model_path)  # Carregar um modelo customizado
    threshold = 0.1

    # Ler a imagem do arquivo
    frame = cv2.imdecode(np.fromstring(image_file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    image_file.seek(0)

    # Processar a imagem com o modelo
    results = model(frame)[0]


    n = 0  # Número de imagens salvas em spots_detected

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
            # Desenha o retângulo
            color = (0, 255, 0) if class_id == 0 else (0, 0, 255)
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 4)

            # Calcula o tamanho do retângulo
            rect_width = x2 - x1
            rect_height = y2 - y1

            # Ajusta o tamanho da fonte com base na largura do retângulo
            font_scale = rect_width / 200  # Ajuste o denominador conforme necessário
            font_scale = max(0.5, font_scale)  # Define um tamanho mínimo para a fonte

            # Desenha o texto
            cv2.putText(frame, f'Prob: {score:.2f}%', (int(x1 + 5), int(y2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), 2)
            
    _, buffer = cv2.imencode('.jpg', frame)
    image_base64 = base64.b64encode(buffer).decode()
    return image_base64


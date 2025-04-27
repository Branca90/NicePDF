from pdf2image import convert_from_path
import os
from paddleocr import PaddleOCR
import cv2
import numpy as np

# Inizializza PaddleOCR
paddle_ocr = PaddleOCR(use_angle_cls=True, lang='en')

# Converti PDF in immagini
images = convert_from_path("data/sample.pdf", dpi=300)
os.makedirs("temp_images", exist_ok=True)

# Salva le immagini e applica PaddleOCR
for i, image in enumerate(images):
    image_path = f"temp_images/page-{i+1:03d}.png"
    image.save(image_path, "PNG")
    print(f"Salvata immagine: {image_path}")

# Esegui OCR con PaddleOCR (solo per debug, non possiamo incorporare direttamente il testo nel PDF)
for i in range(len(images)):
    image_path = f"temp_images/page-{i+1:03d}.png"
    result = paddle_ocr.ocr(image_path, cls=True)
    text = []
    for line in result[0]:
        text.append(line[1][0])
    print(f"Testo estratto dalla pagina {i+1}:\n{' '.join(text)}\n")

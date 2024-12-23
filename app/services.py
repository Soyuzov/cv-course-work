import cv2
import pytesseract

def recognize_text(image_path):
    try:
        # Загрузка изображения
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Could not read the image.")

        # Преобразование изображения в оттенки серого
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Применение порогового значения для улучшения качества OCR
        _, thresh_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY)

        # Использование Tesseract для распознавания текста
        text = pytesseract.image_to_string(thresh_image, lang='rus+eng')

        return text.strip()  # Удаляем лишние пробелы

    except Exception as e:
        raise RuntimeError(f"Error during text recognition: {str(e)}")

import pdfplumber
import pytesseract
from PIL import Image
from io import BytesIO


def extract_text_from_pdf(pdf_path):
    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Извлекаем текст
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
            else:
                # Если текст не извлекся, пытаемся обработать как изображение
                image = page.to_image()
                img_bytes = BytesIO()
                image.save(img_bytes, format="PNG")
                img = Image.open(img_bytes)

                # OCR-распознавание текста с изображения
                ocr_text = pytesseract.image_to_string(img, lang="rus+eng")
                text += ocr_text + "\n"

    return text.strip()

# # Пример использования:
# pdf_text = extract_text_from_pdf("testpdf.pdf")
# print(pdf_text)
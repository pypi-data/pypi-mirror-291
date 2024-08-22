from app.client.classes.OcrClient import OcrClient
from app.ocr.utils.utils import decode_base64_image, draw_text_box

ocr_client = OcrClient(host='http://127.0.0.1:8868')

def run():
    for result in ocr_client.send_pdf(pdf_path='./test/test.pdf', specific_pages=[1, 3, 21]):
        img = decode_base64_image(result['base64_img'])
        draw_text_box(img=img, ocr_results=result['result'])
    

if __name__ == "__main__":
    run()
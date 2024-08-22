from app.client.classes.OcrClient import OcrClient
from PIL import Image
from app.ocr.utils.utils import image_to_base64, decode_base64_image, draw_text_box

ocr_client = OcrClient(host='http://127.0.0.1:8868')

# 載入本地影像
image = Image.open("./test/test.jpg")

img_base64 = image_to_base64(image)
response = ocr_client.send_image(img_base64=img_base64)

# 輸出伺服器的回應
if response.status_code == 200:
    img = decode_base64_image(base64_str=response.json()['base64_img'])
    ocr_result = response.json()['result']
    draw_text_box(img=img, ocr_results=ocr_result)
    
else:
    print(f"Failed to send image. Status code: {response.status_code}")
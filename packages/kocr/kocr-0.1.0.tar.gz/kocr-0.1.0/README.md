# KOCR

![banner](./img/ComfyUI_00081_.png)

## Introduction

PDF 中的資訊難以提取？ 試試 OCR 吧！🤩

PDF 文件中的文字雖然易於閱讀，但想要提取其中的資訊卻常常讓人頭痛😓。別擔心，OCR (光學字符識別) 來救你啦！🙌

**OCR 能將 PDF 文件內的圖像轉換為可編輯的文本內容，並提供每個文字的位置資訊。** 🤯 這意味着你可以輕鬆的：

* 將 PDF 文档中的文字複製到其他應用程式中 📑
* 搜尋 PDF 文件中的特定關鍵字🔎
* 自動整理表格数据📊
* 更有效率地分析和處理文本信息📈

這個專案旨在提供一個方便又實用的解決方案，讓你快速、高效地提取 PDF 文件中的資訊。🚀

採用了 [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR.git) 開源預訓練模型 💪，並搭建了 server 端和 client 端：

* **完全本地運行！** 你不需要連網，任何時候都可以使用它！🌎
* **簡單易用!** 輕鬆架設完成，讓你快速上手 🚀

解鎖 PDF 文件的無限潛力吧！✨

## Pre-require
- [Python](https://www.python.org/downloads/)
- [Docker](https://docs.docker.com/engine/install/ubuntu/)
- 到[PaddleOCR](https://paddlepaddle.github.io/PaddleOCR/ppocr/model_list.html)官網下載相關模型, 模型尺寸請依據各自需求下載, 至少須下載以下3種模型各一個
  - 檢測模型(det)
  - 識別模型(rec)
  - 文本方向分類模型(cls)

## Installation

### pip
TBD

### Docker
1. Build Docker image
```bash
git clone <project_name>
cd kocr
sudo docker build -t kocr:latest .
```

2. Create Docker container
```bash
sudo docker run -d \
--gpus='"device=0"' \
-v /data/models/paddleocr:/data/models/paddleocr \
-e OCR_MODEL_ROOT=/data/models/paddleocr \
-e DET_MODEL=/det/en/en_PP-OCRv3_det_infer \
-e REC_MODEL=/rec/en/en_PP-OCRv4_rec_infer \
-e CLS_MODEL=/cls/ch/ch_ppocr_mobile_v2.0_cls_slim_infer \
-e OCR_PORT=8868 \
-p 8868:8868 \
-w /usr/src/app/kocr \
--restart unless-stopped \
--name kocr \
kocr:latest \
python api_server.py
```

其中 
- `OCR_MODEL_ROOT` 是存放OCR模型的根目錄
- `DET_MODEL` 是存放檢測模型的目錄
- `REC_MODEL` 是存放識別模型的目錄
- `CLS_MODEL` 是存放文本方向分類模型的目錄

Server端預設情況下會去 `{OCR_MODEL_ROOT}{DET_MODEL}` 讀取檢測模型, 沒有的話就會直接下載到該目錄(須連網), 其他兩個模型依此類推。

這邊提供建立容器的範例中以 `-v /data/models/paddleocr:/data/models/paddleocr` 將本機的目錄掛載進容器中, 是因為我將模型放在本機的 `/data/models/paddleocr` 底下, 實際情況可依個人需求進行調整。

`-e OCR_PORT` 則可用來設置server運行的port。

容器建立後server會在背景運行, 例如: http://0.0.0.0:8868。

## Usage

### PDF OCR

```python
from app.client.classes.OcrClient import OcrClient
from app.ocr.utils.utils import decode_base64_image, draw_text_box

ocr_client = OcrClient(host='http://127.0.0.1:8868')

def run():
    for result in ocr_client.send_pdf(pdf_path='./test/test.pdf', specific_pages=[1, 3, 21]):
        img = decode_base64_image(result['base64_img'])
        draw_text_box(img=img, ocr_results=result['result'])
    

if __name__ == "__main__":
    run()
```

### 圖片OCR

```python
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
```
### 滑動視窗OCR (處理較大圖片)
```python
from app.client.classes.OcrClient import OcrClient
from app.ocr.classes import OcrConfig
from PIL import Image
from app.ocr.utils.utils import image_to_base64, decode_base64_image, draw_text_box

ocr_client = OcrClient(host='http://127.0.0.1:8868')

# 載入本地影像
image = Image.open("./test/large.jpg")

img_base64 = image_to_base64(image)
config = {
    "slice":{'horizontal_stride': 300, 'vertical_stride': 500, 'merge_x_thres': 50, 'merge_y_thres': 35}
}
response = ocr_client.send_image(img_base64=img_base64, config=OcrConfig(**config))

# 輸出伺服器的回應
if response.status_code == 200:
    img = decode_base64_image(base64_str=response.json()['base64_img'])
    ocr_result = response.json()['result']
    draw_text_box(img=img, ocr_results=ocr_result)
    
else:
    print(f"Failed to send image. Status code: {response.status_code}")
```
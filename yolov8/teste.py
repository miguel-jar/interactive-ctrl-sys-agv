from ultralytics import YOLO
import cv2

def iterateOverVideo(video_path):
    cap = cv2.VideoCapture(video_path)
    success, img = cap.read()
    fno = 0
    while success:
        success, img = cap.read()
        results = model.predict(img, show=True, save=False, iou=0.2, )  # predict on an image
    
    
if __name__ == '__main__':
    
    misturado = "modelos/v1_cor_com_grayscale/best.pt"
    grayscale = "modelos/v1_full_grayscale/best.pt"
    normal_v4 = "modelos/v4/best.pt"
    
    obb_v1 = "modelos/obb_v1/best.pt"
    obb_v2 = "modelos/obb_v2/best.pt"
    obb_v3 = "modelos/obb_v3/best.pt"
    obb_v4 = "modelos/obb_v4/best.pt"
    obb_v5 = 'modelos/obb_v5/best.pt'
    
    fotos = "fotos/percurso1/*.jpg"
    video = "videos/tcc_reduzido.mp4"

    model = YOLO(obb_v5)  # load a custom model

    # iterateOverVideo(video_path)
    
    results = model.predict(fotos, imgsz=(736, 736), show=False, save=False, iou=0.4)  # predict on an image
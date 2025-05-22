import cv2
import numpy
import os
from PIL import Image
import imageio
import torch
from ultralytics import YOLO

model = YOLO('best.pt')
device = 'cuda' if torch.cuda.is_available() else 'cpu'

def extract_main_eyes(image_path):
    ddsimg = Image.open(image_path)
    if ddsimg is None:
        return []

    ddsimg = ddsimg.convert("RGB")
    img_np = numpy.array(ddsimg)
    original_h, original_w = img_np.shape[:2]

    results = model(img_np, device=device)
    
    boxes = results[0].boxes
    if boxes is None or boxes.data is None or len(boxes.data) == 0:
        print("No detections found.")
        return []
    eyes = []

    CONF_THRESH = 0.95
    high_conf = [b for b in boxes.data if b[4] >= CONF_THRESH]
    low_conf = [b for b in boxes.data if b[4] < CONF_THRESH]
    
    high_conf_sorted = sorted(high_conf, key=lambda b: (int(b[0]), int(b[1])))
    low_conf_sorted = sorted(low_conf, key=lambda b: -b[4])
    
    sorted_boxes = high_conf_sorted + low_conf_sorted
    
    for box in sorted_boxes:
        x1, y1, x2, y2, conf, cls = box.tolist()
        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
        w = x2 - x1
        h = y2 - y1
        cx = x1 + w // 2
        cy = y1 + h // 2

        roi = img_np[y1:y2, x1:x2]
        mask = numpy.zeros((h, w), dtype=numpy.uint8)
        cv2.ellipse(mask, (w // 2, h // 2), (w // 2, h // 2), 0, 0, 360, 255, -1)

        roi_bgra = roi.copy()
        if roi_bgra.shape[2] == 3:
            roi_bgra = cv2.cvtColor(roi_bgra, cv2.COLOR_RGB2RGBA)
        roi_bgra[:, :, 3] = mask

        eyes.append(roi_bgra)
        
    return eyes

def create_eye_texture_on_dots(eyes, output_size = (512, 1024)):
    output = numpy.zeros((output_size[1], output_size[0], 4), dtype=numpy.uint8)
    
    dot_positions = [(int(output_size[0] * 0.486), int(output_size[1] * 0.228)), (int(output_size[0] * 0.514), int(output_size[1] * 0.733))]
    
    if len(eyes) == 0:
        return output
    elif len(eyes) == 1:
        eyes = [eyes[0], eyes[0]]
    else:
        eyes = eyes[:2]
        
    for i, eye_img in enumerate(eyes):
        dot_x, dot_y = dot_positions[i]
        h, w, _ = eye_img.shape
        new_w = int(output_size[0] * 0.514)
        new_h = int(h * (new_w / w))
        
        eye_img = cv2.resize(eye_img, (new_w, new_h))
        
        top_left_x = dot_x - new_w // 2
        top_left_y = dot_y - new_h // 2
        
        output[top_left_y:top_left_y+new_h, top_left_x:top_left_x+new_w] = eye_img
    
    return output

def create_new_texture_size(image_path):
    ddsimg = Image.open(image_path)
    if ddsimg is None:
        return [512, 1024]
        
    ddsimg = ddsimg.convert("RGBA")
    
    img = numpy.array(ddsimg)
        
    h, w = img.shape[:2]
    
    lowlen = 0
    if h >= w:
        lowlen = h
    else:
        lowlen = w
        
    if lowlen >= 1024:
        if lowlen == h:
            w = int(w * (1024 / h))
            h = 1024
        elif lowlen == w:
            h = int(h * (1024 / w))
            w = 1024
    
    if w > h:
        tmp = w
        w = h
        h = tmp
        
    if w < 512:
        w = 512
    if h < 1024:
        h = 1024
        
    if h >= w * 2:
        w = h // 2
    else: #h < w * 2
        h = w * 2
    return [w, h]

def process_images(input_folder, output_folder):
    for root, dirs, files in os.walk(input_folder):
        for filename in files:
            if filename.lower().endswith(('.dds', '.png', '.jpg')):
                input_path = os.path.join(root, filename)
                
                rel_path = os.path.relpath(root, input_folder)
                output_subfolder = os.path.join(output_folder, rel_path)
                if not os.path.exists(output_subfolder):
                    os.makedirs(output_subfolder)
                
                output_path = os.path.join(output_subfolder, filename)
                
                eyes = extract_main_eyes(input_path)
                if len(eyes) == 0:
                    continue
                final_texture = create_eye_texture_on_dots(eyes, create_new_texture_size(input_path))
                
                output_path, ext = os.path.splitext(output_path)
                output_path = output_path + ".dds"
                imageio.imwrite(output_path, final_texture, format="DDS")
                print(f"Saved processed image to {output_path}")

def main():
    input_folder = "input"
    output_folder = "output"
    process_images(input_folder, output_folder)

if __name__ == "__main__":
    main()

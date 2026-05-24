import numpy as np
from PIL import Image

def preprocess_image(img, target_size=(224, 224)):
    """
    Preprocess a PIL image for CNN model prediction.
    - Converts to RGB
    - Resizes to target_size
    - Normalizes pixel values to [0, 1]
    - Expands dims for batch prediction
    """
    if img.mode != "RGB":
        img = img.convert("RGB")
    
    img = img.resize(target_size)
    img_array = np.array(img, dtype=np.float32)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

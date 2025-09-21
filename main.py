from fastapi import FastAPI, UploadFile, File
from tensorflow.keras.preprocessing import image

from tensorflow.keras.models import load_model
from tensorflow.keras.utils import img_to_array
import numpy as np
from PIL import Image
import io

import os
MODEL_PATH = os.path.join(os.path.dirname(__file__), "pneumonia_model.h5")
model = load_model(MODEL_PATH)

# Create API
app = FastAPI(title="Pneumonia Detection API !!!Updated!!")

# Preprocessing function
def preprocess(img):
    img = img.resize((224, 224))
    img_array = image.img_to_array(img)  # works now
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    img = Image.open(io.BytesIO(contents)).convert("RGB")

    # Preprocess
    input_data = preprocess(img)

    # Predict
    preds = model.predict(input_data)
    prob = float(preds[0][0])  # assuming binary classification
    label = "Pneumonia" if prob > 0.5 else "Normal"

    return {"prediction": label, "confidence": prob}




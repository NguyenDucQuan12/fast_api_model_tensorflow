import tensorflow as tf
import cv2
import numpy as np

image = cv2.imread(".FastAPI/assets/malaria.png")

load_save_model = tf.keras.models.load_model(".FastAPI/service/core/logic/Malaria_model_save.keras")

test_image = cv2.resize(image, (224, 224))
im = np.float32(test_image)
image_predict = np.expand_dims(im, axis= 0)
# print(load_save_model.summary())
print("hình ảnh đầu vào có kích thước")
print(image_predict.shape)
print("Bắt đầu dự đoán")
predicted = load_save_model.predict(image_predict)
print(predicted[0][0])
import numpy as np
import cv2
import time
import service.main as s
# from service.main import load_save_model #sẽ gây ra lỗi (most likely due to a circular import) có khả năng do tên main trùng


def emotion_model(image):

    # Mỗi lần dự đoán là một lần tải model, có thể chuyển sang load model ở file main để ko cần load lại
    # time_load_model_start = time.time()
    # load_save_model = tf.keras.models.load_model(".FastAPI/service/core/logic/Malaria_model_save.keras")
    # time_elapsed_load_model = time.time() - time_load_model_start
    # print(time_elapsed_load_model)

    time_load_img = time.time()

    test_image = cv2.resize(image, (224, 224))
    im = np.float32(test_image)

    image_predict = np.expand_dims(im, axis= 0)

    # print(load_save_model.summary())
    # print("hình ảnh đầu vào có kích thước")
    # print(image_predict.shape)
    # print("Bắt đầu dự đoán")

    predicted = s.load_save_model.predict(image_predict)

    time_elapsed_predict = time.time()-time_load_img
  
    
    # Numpy.float32 không thể lặp lại nên cần phải chuyển qua loại int mới chạy được
    if int(predicted[0][0]) == 0:
        result = "Ung thư"
    else:
        result = "Không ung thư"
    return {
        "emotion": result,
        "time_elapsed_predict": str(time_elapsed_predict)
    }

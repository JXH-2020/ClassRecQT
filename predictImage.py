import operator

import cv2
import onnxruntime
import torch
import torchvision.transforms as transforms


def to_numpy(tensor):
    return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()


def loadModel(modelPath):

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    DEVICE_TYPE = device.__str__()
    if DEVICE_TYPE == 'gpu':
        providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
    else:
        providers = ['CPUExecutionProvider']

    # 初始化 加载性别年龄检测模型
    deepsort_session = onnxruntime.InferenceSession(modelPath, providers=providers)
    return deepsort_session


def predict(image, deepsort_session):
    class_ = ['Mosaic', 'Rust', 'Grey_spot', 'Brown_Spot', 'Alternaria_Boltch']
    to_tensor = transforms.ToTensor()
    img = to_tensor(cv2.resize(image, (224, 224))).unsqueeze_(0)
    inputs = {deepsort_session.get_inputs()[0].name: to_numpy(img)}
    gender_pd = deepsort_session.run(None, inputs)
    max_index, max_number = max(enumerate(gender_pd[0][0]), key=operator.itemgetter(1))
    return class_[max_index]

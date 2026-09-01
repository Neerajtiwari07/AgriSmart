import pickle


MODEL_PATH = "models/crop_model.pkl"


with open(MODEL_PATH, "rb") as f:
    crop_model = pickle.load(f)
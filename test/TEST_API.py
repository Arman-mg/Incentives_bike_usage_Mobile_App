import requests 
import pickle 
from PIL import Image
import os 
# get the path of the current file
File_PATH = os.path.dirname(os.path.abspath(__file__))
name_img = "bike.jpg"
Image_path = os.path.join(File_PATH,"test_images",name_img)


image = Image.open(Image_path)
image=image.convert("RGB")

Serialized = pickle.dumps(image)
files = {'image': (name_img, Serialized, 'multipart/form-data', {'Expires': '0'})}
resp = requests.get('http://127.0.0.1:5000/bike_detection',files = files)
print(resp.json())

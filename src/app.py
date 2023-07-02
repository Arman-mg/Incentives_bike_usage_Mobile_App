from flask import Flask , request ,jsonify
import numpy as np 
import logging
import traceback
import pickle
from Bike_Detector import BICI_DETECTOR
from GPS_AC import *

DETECTOR = BICI_DETECTOR()




def prepare_1(img):
    image_np = np.asarray(img)
    return image_np



app = Flask(__name__)

   
@app.route('/bike_detection', methods = ["GET"])
def bike_detection():
    if request.method == "GET": 
        file = request.files['image']
        if file is  None or file.filename == "": 
            return jsonify({"error":"no file"})
        
        try: 
            img = pickle.loads(file.read()) 
            
            image = prepare_1(img)
            result = DETECTOR.detect_multi_object(image,score_threshold=0.4)
            return jsonify({"result": True if  len(result)> 0 else False })
        except Exception as e:
            logging.error(traceback.format_exc())
            return jsonify({{'error':str(e)}})
    return 'OK'


@app.route('/gps_detection', methods = ["GET"])
def gps_anti_cheating(): 
    if request.method == "GET":
        file = request.get_json()
        if file is  None or file.filename == "": 
            return jsonify({"error":"no file"})
        
        try : 
            count = 0
            cheating_df = findSpeed(file)
            for i in cheating_df:  
                if i["cheating"] == True: 
                    count+=1
                if count >= 3: 
                    return jsonify({"cheating": True})
            return jsonify({"cheating": False})
        except Exception as e:
            return jsonify({{'error':str(e)}})
    return 'OK'


if __name__ == "__main__": 
    
      app.run(host='127.0.0.1', port=5000, debug=True )






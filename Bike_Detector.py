import tensorflow as tf 
import os
import numpy as np 


MODEL_NAME = 'faster_rcnn_resnet101_coco_11_06_2017' # for improved accuracy
MODEL_PATH = os.getcwd()
PATH_TO_CKPT = os.path.join(MODEL_PATH,MODEL_NAME,'frozen_inference_graph.pb')

class BICI_DETECTOR(object):
    def __init__(self)-> None:
        self.detection_graph = self.load_graph()
        self.extract_graph_components()
        self.sess = tf.compat.v1.Session(graph=self.detection_graph)

        # run the first session to "warm up"
        dummy_image = np.zeros((100, 100, 3))
        self.detect_multi_object(dummy_image, 0.1)
        self.traffic_light_box = None
        self.classified_index = 0
    
    
    @staticmethod
    def load_graph():
        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.compat.v1.GraphDef()
            # od_graph_def = tf.saved_model.load()
            with tf.io.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        return detection_graph
    
    @staticmethod
    def select_boxes(boxes : np.ndarray, classes : np.ndarray, scores : np.ndarray, score_threshold=0, target_class=2)-> np.ndarray:
        """
        :param boxes:
        :param classes:
        :param scores:
        :param target_class: default traffic light id in COCO dataset is 10
        :return:
        """

        sq_scores = np.squeeze(scores)
        sq_classes = np.squeeze(classes)
        sq_boxes = np.squeeze(boxes)

        sel_id = np.logical_and(sq_classes == target_class, sq_scores > score_threshold)

        return sq_boxes[sel_id]
    
    def extract_graph_components(self):
        # Definite input and output Tensors for detection_graph
        self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
        # Each box represents a part of the image where a particular object was detected.
        self.detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
        # Each score represent how level of confidence for each of the objects.
        # Score is shown on the result image, together with the class label.
        self.detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
        self.detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
        self.num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

    def detect_multi_object(self, image_np : np.ndarray, score_threshold:float) -> np.ndarray :
        """
        Return detection boxes in a image

        :param image_np: np.ndarray
        :param score_threshold:float
        :return sel_boxes : np.ndarray
        """

        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image_np, axis=0)
        # Actual detection.
        print(np.shape(image_np_expanded))
        (boxes, scores, classes, _) = self.sess.run(
            [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
            feed_dict={self.image_tensor: image_np_expanded})

        sel_boxes = self.select_boxes(boxes=boxes, classes=classes, scores=scores,
                                 score_threshold=score_threshold, target_class=2)

        return sel_boxes
import cv2
import os
import time
import json
from scenedetect import detect, ContentDetector
from darkflow.net.build import TFNet
from parser import Parser


class ADGenerator:
    def __init__(self):
        self.video_input = Parser().input
        self.results_out_path = Parser().output
        self.final_result = {}


    def video_analysis(self):
        frames = self.analyze_shot()
        self.split_frames(frames, self.video_input)
        # print(self.final_result)

    def write_shots(self, list_shot):
        path = self._path_exists("\shots")
        f = open(path+"\change_shots_detected.json", "w")
        f.write(',\n'.join(list_shot))
        f.close()

    def predict_midia():


        options = {"model": "cfg/yolo.cfg", "load": "bin/yolo.weights", "threshold": 0.1}

        tfnet = TFNet(options)

        imgcv = cv2.imread("./sample_img/sample_dog.jpg")
        result = tfnet.return_predict(imgcv)
        print(result)

    def analyze_shot(self):
        scene_list = detect(self.video_input, ContentDetector())
        list_frames = []
        shot_frames = []
        for i, scene in enumerate(scene_list):
            value = f'"Scene": {i+1}, "Start": ["{scene[0].get_timecode()}", "{scene[0].get_frames()}"], "End": ["{scene[1].get_timecode()}", "{scene[1].get_frames()}"]'
            shot_frames.append(value) #ver se vai ser utilizado esse dado
            list_frames.append(scene[0].get_frames())
        
        self.write_shots(shot_frames)
       
        return list_frames
    
    def write_frame(self, cap, frame, directory):
        try:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
            ret, _frame = cap.read()
            path = directory+f"/frame_{frame}.jpg"
            cv2.imwrite(path, _frame)
            if f"frame_{frame}.jpg" not in self.final_result:
                self.final_result[f"frame_{frame}.jpg"] = {"labels": [], "text_from_labels": "", "text_from_image": "", "audio_url": ""}
        except:
            pass # for null frames
    
    def _path_exists(self, directory):
        if not os.path.exists(self.results_out_path+directory):
            os.makedirs(self.results_out_path+directory)
        return self.results_out_path+directory

    def split_frames(self, frame_list, video_path):
        cap = cv2.VideoCapture(video_path)

        for frame in frame_list:
            self.write_frame(cap, frame, self._path_exists("/train"))

        cap.release()
        cv2.destroyAllWindows() # destroy all opened windows

if __name__ == "__main__":
    adg = ADGenerator()
    adg.video_analysis()
    # adg.split_frames()

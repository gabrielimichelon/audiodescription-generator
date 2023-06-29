import cv2
import os
import time
import json
import re
from scenedetect import detect, ContentDetector
from integration.darkflow.net.build import TFNet #https://github.com/thtrieu/darkflow
from parser import Parser

class ADGenerator:
    def __init__(self):
        self.video_input = Parser().input
        self.results_out_path = Parser().output
        self.final_result = {}
        self.images_list = []
        self.numbers = re.compile(r'(\d+)')
        self.train_dir = './src/results/train/'
        self.label_dir = './src/results/label/'


    def video_analysis(self):
        frames = self.analyze_shot()
        self.split_frames(frames, self.video_input)
        # print(self.final_result)
        
        self.predict_midia()

    def write_shots(self, list_shot):
        path = self._path_exists("\shots")
        f = open(path+"\change_shots_detected.json", "w")
        f.write(',\n'.join(list_shot))
        f.close()

    def numericalSort(self, value):
        parts = self.numbers.split(value)
        parts[1::2] = map(int, parts[1::2])
        return parts

    def get_list_dir(self):
        files = [file for file in os.listdir(self.train_dir)]
        files = sorted(files, key=self.numericalSort)
        return files

    def predict_midia(self):

        options = {"model": "integration/cfg/yolov2.cfg", "load": "integration/bin/yolov2.weights", "threshold": 0.1, "gpu": 1.0}
        options = {"model": "integration/cfg/yolov2.cfg", "threshold": 0.1, "gpu": 1.0, "train": True, "trainer": "adam", "annotations": self.label_dir}
        tfnet = TFNet(options)
        
        # imgcv = cv2.imread("./integration/sample_img/sample_dog.jpg")
        for path in self.get_list_dir():
            print(f" PATH : {self.train_dir+path}")
            imgcv = cv2.imread(self.train_dir+path)

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

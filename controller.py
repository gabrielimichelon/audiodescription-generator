import cv2
import os
import time
from scenedetect import detect, ContentDetector
from parser import Parser

class ADGenerator:
    def __init__(self):
        self.video_input = Parser().input
        self.results_out_path = Parser().output
        self.final_result = {}


    def video_analysis(self):
        frames = self.analyze_shot()
        self.split_frames(frames, self.video_input, self.results_out+"/frames/")


    def analyze_shot(self):
        scene_list = detect(self.video_input, ContentDetector())
        print(scene_list)
        for i, scene in enumerate(scene_list):
            print('    Scene %2d: Start %s / Frame %d, End %s / Frame %d' % (
            i+1,
            scene[0].get_timecode(), scene[0].get_frames(),
            scene[1].get_timecode(), scene[1].get_frames(),))

    def distinct_img(self):
        pass
    
    def write_frame(self):
        pass

    def split_frames(self, frames_list, video_path, frames_path):
        cap = cv2.VideoCapture(f"{video_path}")
        
        if not os.path.exists(frames_path):
            os.makedirs(frames_path)

        for frame in frame_list:
            self.write_frame(cap, frame, directory)

        cap.release()
        cv2.destroyAllWindows() # destroy all opened windows

if __name__ == "__main__":
    adg = ADGenerator()
    adg.video_analysis()
    # adg.split_frames()

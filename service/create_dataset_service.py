import cv2
from scenedetect import detect, ContentDetector
from validation.dir_validation import ValidDir

class CreateDataset:
    def __init__(self, input, output) -> None:
        self.video_input = input
        self.results_out_path = output
        self.final_result = {}

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

    def write_shots(self, list_shot):
        path = ValidDir.path_exists("\shots", self.results_out_path)
        f = open(path+"\change_shots_detected.json", "w")
        f.write(',\n'.join(list_shot))
        f.close()

    def split_frames(self, frame_list, video_path):
        cap = cv2.VideoCapture(video_path)

        for frame in frame_list:
            self.write_frame(cap, frame, ValidDir.path_exists("/train", self.results_out_path))

        cap.release()
        cv2.destroyAllWindows() # destroy all opened windows

    def create_dataset_train(self):
        frames = self.analyze_shot()
        self.split_frames(frames, self.video_input)
        # print(self.final_result)

    def write_frame(self, cap, frame, directory):
        try:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
            ret, _frame = cap.read()
            path = directory+f"/frame_{frame}.jpg"
            cv2.imwrite(path, _frame)
            # if f"frame_{frame}.jpg" not in self.final_result:
            #     self.final_result[f"frame_{frame}.jpg"] = {"labels": [], "text_from_labels": "", "text_from_image": "", "audio_url": ""}
        except:
            pass # for null frames
    
    

  
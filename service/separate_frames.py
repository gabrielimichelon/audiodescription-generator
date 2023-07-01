import cv2
from validation.dir_validation import ValidDir

class SeparateFrames:
    def __init__(self):
        self.final_result = {}

    def get_frames(self, video_path, results_out_path):
        cap = cv2.VideoCapture(video_path)
        frame = 0
        for frame in range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))):
            self.write_frame(cap, ValidDir.path_exists("/all_frames", results_out_path), frame)
        cap.release()
        cv2.destroyAllWindows() # destroy all opened windows

    def write_frame(self, cap, directory, frame):
        try:
            ret, _frame = cap.read()
            path = directory+f"/frame_{frame}.jpg"
            cv2.imwrite(path, _frame)
            if f"frame_{frame}.jpg" not in self.final_result:
                self.final_result[f"frame_{frame}.jpg"] = {"labels": [], "text_from_labels": "", "text_from_image": "", "audio_url": ""}
        except:
            pass # for null frames

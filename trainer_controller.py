import os

class Trainner:
    def __init__(self) -> None:
        self.train_img_path = "/content/images/train"
        self.val_img_path = "/content/images/val"

    def training_img(self):
        with open('train.txt', "a+") as f:
            img_list = os.listdir(self.train_img_path)
            for img in img_list:
                f.write(os.path.join(self.train_img_path,img+'\n'))
            print("Done")
    
    def validation_img(self):
        with open('val.txt', "a+") as f:
            img_list = os.listdir(self.val_img_path)
            for img in img_list:
                f.write(os.path.join(self.val_img_path,img+'\n'))
            print("Done")
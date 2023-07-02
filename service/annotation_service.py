import os
import re
import glob
import json
from roboflow import Roboflow

'''
    Update das imagens para o novo Dataset. É necessário entrar na API online e gerar as anotações manualmente
    https://docs.roboflow.com/api-reference/images/upload-api#parameters-annotations

    Parameters:
    - project_name: Preferred project name.
    - project_type: Must be one of object-detection, single-label-classification, multi-label-classification, instance-segmentation, or semantic-segmentation.
    - project_description: Preferred project description.
'''

class AnnotationBoundingBox:

    def __init__(self):
        self.PROJECT_NAME = self.set_project_name()
        

    def set_project_name(self):
        return input("Insira o nome do projeto no Roboflow: ")
       
    # def set_workspace(self):
    #     return input("Insira o nome do workspace no Roboflow: ")
    
    def types(self):
        op = {
            1: "object-detection", 
            2: "single-label-classification", 
            3: "multi-label-classification", 
            4: "instance-segmentation",
            5: "semantic-segmentation"
        }
        for key in op.keys():
            print(key, '--', op[key] )
        

    def set_project_type(self):       
        self.types()
        op = ''
        try:
            op = int(input('Enter your choice: '))
            print(op)
        except:
            print('Wrong input. Please enter a number ...')
        if op == 1:
            return "object-detection"
        elif op == 2:
            return "single-label-classification"
        elif op == 3:
            return "multi-label-classification"
        elif op == 4:
            return "instance-segmentation"
        elif op == 5:
            return "semantic-segmentation"
   
    def read_path(self, dir_name):
        images_list = []
        for directory, subdir, files in os.walk(dir_name):
            print(files)
            files = sorted(files, key=self.numericalSort)
            print(files)
            for arquivo in files:
                path_img = os.path.join(directory, arquivo)
                print(arquivo)
                if ".jpg" in path_img:
                    print(path_img)
                    images_list.append(path_img)
                    #print(path_img)
        return images_list

    # def update_imgs(self, ws):
        
    #     # Directory path and file extension for images
    #     dir_name = "./src/results/train/images"
    #     file_extension_type = ".jpg"
    #     # Get the upload project from Roboflow workspace
    #     print(ws.name)
    #     # upload_project = ws.project(self.PROJECT_NAME)

    #     # Upload images
    #     image_glob = glob.glob(dir_name + '/*' + file_extension_type)
    #     files = self.read_path(dir_name)
    #     print(files)
    #     ws.upload_dataset()
    #     for image_path in files:
    #         print(ws.project(self.PROJECT_NAME).upload_file(image_path))
    
    #ordenador
    def numericalSort(self, value):
        numbers = re.compile(r'(\d+)')
        parts = numbers.split(value)
        parts[1::2] = map(int, parts[1::2])
        return parts


    def verify_project(self, ws):
        for proj in ws.project_list:
            if self.PROJECT_NAME == proj['name']:
                return True
            else:
                return False
    
    def create_job2annotation(self):
        rf = Roboflow(api_key=os.environ.get('KEY_ROBOFLOW'))
        
        dir_name = "./src/results/train/images"

        workspace = rf.workspace()
        
        if self.verify_project(workspace):
            files = self.read_path(dir_name)
            print(files)
            for image_path in files:
                print(workspace.upload_file(image_path, self.PROJECT_NAME, project_license="Public Domain"))
                
        else:
            print("else")
            TYPE_PROJECT = self.set_project_type()
            workspace.create_project(project_name= self.PROJECT_NAME, project_type=TYPE_PROJECT, project_license="Public Domain", annotation=self.PROJECT_NAME)
            files = self.read_path(dir_name)
            print(files)
            for image_path in files:
                print(workspace.upload_dataset(image_path, self.PROJECT_NAME, project_license="Public Domain", project_type=TYPE_PROJECT))


        
        


if __name__ == "__main__":
    an = AnnotationBoundingBox()
    an.create_job2annotation()
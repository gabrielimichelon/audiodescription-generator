import cv2
import os
import time
import json
import re
from service.parser import Parser
from ultralytics import YOLO
from roboflow import Roboflow
from IPython.display import display, Image


class ADGenerator:
    def __init__(self, input, output):
        self.video_input = input
        self.results_out_path = output
        self.images_list = []
        
        self.train_dir = './src/results/train/'
        self.label_dir = './src/results/label/'


    def video_analysis(self):
        pass
        # self.predict_midia()

    
    #ordenador
    def numericalSort(self, value):
        numbers = re.compile(r'(\d+)')
        parts = numbers.split(value)
        parts[1::2] = map(int, parts[1::2])
        return parts
    
    #lista de arquivos da pasta em ordem numerica
    def get_list_dir(self):
        files = [file for file in os.listdir(self.train_dir)]
        files = sorted(files, key=self.numericalSort)
        return files

    def create_dataset(self):        
        # api_key="cjzb26hIzcknpaAh9Mo5"
        print(os.getenv('KEY_ROBOFLOW'))
        rf = Roboflow(api_key=os.environ.get('KEY_ROBOFLOW'))
        project = rf.workspace("uergs").project("comercial-teste")
        dataset = project.version(1).download("yolov8", './src/dataset_train/')


    def predict_midia(self):

        # Carregar um modelo
        # model = YOLO( 'yolov8n.yaml' )   # construir um novo modelo a partir do zero
        # model = YOLO( 'yolov8n.pt' )   # carregar um modelo pré-treinado (recomendado para treinamento) # Usar os resultados 
        model = YOLO(f'./src/model/yolov8s-seg.pt')
        # Uso do modelo
        results = model.train(data='coco128.yaml' , epochs= 3)   # treina o modelo
        results = model.val()   # avalia o desempenho do modelo no conjunto de validação
        results = model(self.video_input)   # prever em uma imagem
        sucesso = model.export(format = 'onnx')   # exporta o modelo para o formato ONNX

    
    
    
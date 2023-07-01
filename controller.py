import cv2
import os
import time
import json
import re
import emoji
from service.parser import Parser
from ultralytics import YOLO
from roboflow import Roboflow
from IPython.display import display, Image
from service.adgenerator_service import ADGenerator
from service.parser import Parser
from service.create_dataset_service import CreateDataset
from service.separate_frames import SeparateFrames

video_input = Parser().input
results_output = Parser().output

menu_options = {
    1: f'Criar dataset para treino {emoji.emojize(":floppy_disk:")}' ,
    2: f'Dividir frames {emoji.emojize(":scissors:")}',
    3: f'Treinar {emoji.emojize(":mechanical_arm:")}',
    4: f'Gerar AD {emoji.emojize(":speaking_head:")}',
    5: f'Exit {emoji.emojize(":person_running:")}',
}

def print_menu():
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )

def option1():
    CreateDataset(video_input, results_output).create_dataset_train()
    print(f'DONE {emoji.emojize(":check_mark_button:")}\n')

def option2():
    SeparateFrames().get_frames(video_input, results_output)
    print(f'DONE {emoji.emojize(":check_mark_button:")}\n')

def option3():
    # self.create_dataset()
    print(f'DONE {emoji.emojize(":check_mark_button:")}\n')

def option4():
    adg = ADGenerator(video_input, results_output)
    adg.video_analysis()
    print(f'DONE {emoji.emojize(":check_mark_button:")}\n')


if __name__=='__main__':
    while(True):
        print_menu()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
        #Check what choice was entered and act accordingly
        if option == 1:
           os.system('cls')
           option1()
        elif option == 2:
            os.system('cls')
            option2()
        elif option == 3:
            os.system('cls')
            option3()
        elif option == 4:
            os.system('cls')
            option4()
        elif option == 5:
            print(f'Thanks {emoji.emojize(":waving_hand:")}')
            exit()
        else:
            print('Invalid option. Please enter a number between 1 and 4.')
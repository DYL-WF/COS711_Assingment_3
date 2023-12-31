from abc import abstractmethod
import pandas as pd
import numpy as np

import random
import logging

import torch
import torchvision

np.set_printoptions(precision=3, suppress=True)
logging.basicConfig( filename='./logs/debug.log', level=logging.DEBUG)
logging.FileHandler(filename='./logs/debug.log',mode='w')
class data_engine():
    def __init__(self, file_path, mode="train"):

        logging.info("# Initalizing data engine for file: "+file_path)
        self.file_path = file_path
        self.data = pd.read_csv(
                file_path,
                header=0,
                sep=",",
                index_col=0,
            )
        self.mode = mode
        
        # Normalizing the extent attribute
        self.data['extent'] = self.data['extent'].div(100)
        
        logging.debug("Raw Data")
        logging.debug(self.data)
    
    def get_image_data(self,file_name):
        img = torchvision.io.read_image("content/"+self.mode+"/"+file_name)
        return img

    def get_input(self, index: int):

        logging.info("# retrieving data for row: "+str(index))
        if((index < self.data.count().count()) & (index >= 0)):
            img_data = self.get_image_data(self.data.iloc[index]["filename"])       
            meta_data = self.data.iloc[index].to_list()[1:]

            logging.debug("Image data: ")
            logging.debug(img_data)
            logging.debug("Meta data: ")
            logging.debug(meta_data)
            return img_data, meta_data
        else:
            logging.error("Index out of bounds")
            raise Exception("Index out of bounds")
    
    #TRANSFORMATIONS
    def one_hot_encode(self):
        logging.info("# One-hot encoding enbaled")

        #Get one hot extension for each categorical attribute
        OH_growth_stage = pd.get_dummies(self.data['growth_stage'])
        OH_damage = pd.get_dummies(self.data['damage'])
        OH_season = pd.get_dummies(self.data['season'])

        #Drop attributes
        self.data = self.data.drop(columns=["growth_stage"])
        self.data = self.data.drop(columns=["damage"])
        self.data = self.data.drop(columns=["season"])

        # Append one hot encodings
        self.data = pd.concat([self.data, OH_growth_stage],axis=1)
        self.data = pd.concat([self.data, OH_damage],axis=1)
        self.data = pd.concat([self.data, OH_season],axis=1)

        logging.debug(self.data)


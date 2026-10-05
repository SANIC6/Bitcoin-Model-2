import pandas as pd
import numpy as np
import logging
import requests
import torch
from torch.utils.data import DataLoader, TensorDataset

#--- Logger set up -------------------------
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
#--------------------------------




class DataExtractor:
    """
        
    """
    def __init__(self) -> None:
        pass
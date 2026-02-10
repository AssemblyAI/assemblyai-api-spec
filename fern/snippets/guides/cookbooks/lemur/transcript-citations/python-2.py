import datetime
import numpy as np
import requests
import time
from sklearn.neighbors import NearestNeighbors
from sentence_transformers import SentenceTransformer

# Configuration
api_key = "<YOUR_API_KEY>"
base_url = "https://api.assemblyai.com"
headers = {"authorization": api_key}

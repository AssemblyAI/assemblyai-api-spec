import os
import assemblyai as aai
from pyannote.audio import Pipeline
import torch
import pandas as pd
import numpy as np

# Assign your API keys
HUGGING_FACE_TOKEN = os.getenv("HF_TOKEN")
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

# Authenticate with AssemblyAI
aai.settings.api_key = ASSEMBLYAI_API_KEY

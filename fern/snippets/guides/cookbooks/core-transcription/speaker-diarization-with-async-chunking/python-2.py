import assemblyai as aai
import requests
import json
import time
import requests
import copy
from pydub import AudioSegment
import os
import nemo.collections.asr as nemo_asr

speaker_model = nemo_asr.models.EncDecSpeakerLabelModel.from_pretrained("nvidia/speakerverification_en_titanet_large")

assemblyai_key = "YOUR_API_KEY"

headers = {
    "authorization": assemblyai_key
}

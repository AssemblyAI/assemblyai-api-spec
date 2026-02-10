import requests
import json
import os
import csv
import time
import re

# Configuration
api_key = "<YOUR_API_KEY>"
base_url = "https://api.assemblyai.com"
headers = {"authorization": api_key}
output_filename = "profiles.csv"

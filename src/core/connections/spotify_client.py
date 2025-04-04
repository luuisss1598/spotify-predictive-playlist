import logging
from dotenv import load_dotenv, find_dotenv
import os 
from typing import Dict, Any, List, Optional
import datetime

# class SpotifyClient:
#     BASE_URL = ''

#     def __init__(self, client_id: str, client_secret: str):
#         self.client_id = client_id
#         self.client_secret = client_secret

#     def authenticate(self):
#         pass



# env_path = find_dotenv(filename='.env')
# load_dotenv(env_path)

# api_client_id = os.getenv('SPOTIFY_CLIENT_ID')

def get_time():
    current_time = datetime.datetime.now()

    return current_time
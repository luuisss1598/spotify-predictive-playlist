"""
Basic example of what a config file might look like
"""

# src/core/config.py
# import os
# from dotenv import load_dotenv

# class AppSettings:
#     def __init__(self):
#         # Load environment variables
#         load_dotenv()
        
#         # Sensitive configurations from env variables
#         self.spotify_credentials = {
#             "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
#             "client_secret": os.getenv("SPOTIFY_CLIENT_SECRET")
#         }
        
#         # Application settings (could be from yaml if needed)
#         self.pipeline_settings = {
#             "batch_size": 1000,
#             "max_songs": 50,
#             "update_frequency": 24
#         }

# # Usage
# settings = AppSettings()
# spotify_client = SpotifyClient(
#     client_id=settings.spotify_credentials["client_id"],
#     client_secret=settings.spotify_credentials["client_secret"]
# )


from connections.spotify import get_current_time

print(get_current_time())
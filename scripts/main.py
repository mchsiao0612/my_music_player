from music_player import Music_Player

# Set information for credential authentication.
client_secret_file = "../credentials/client_secret.json"
api_name, api_version, scopes = "drive", "v3", ["https://www.googleapis.com/auth/drive"]

# Instantiate a music player and launch the application.
player = Music_Player(client_secret_file, api_name, api_version, scopes, music_folder_name="Music")
player.start()


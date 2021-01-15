import sys
import os
import io
import pickle
import vlc
from simple_term_menu import TerminalMenu
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request

class Music_Player:

    # Constructor.
    def __init__(self, client_secret_file, api_name, api_version, scopes, music_folder_name="Music"):
        
        # Initialize the information to authenticate.
        self.client_secret_file = client_secret_file
        self.api_name = api_name
        self.api_version = api_version
        self.scopes = scopes

        # Initialize the service instance.
        self.service_instance = None
        self.is_application_quit = False

        # Initialize the root music folder.
        self.music_folder_name = music_folder_name
        self.music_folder_id = None

        # Initialize the menu.
        self.current_menu = None
        self.current_menu_name = None
        self.selected_index = None

        # Initialize the recorded music and playlist.
        self.all_music = None
        self.all_playlist = None

        # Initialize the downloader.
        self.file_stream = None
        self.downloader = None

        # Initialize the vlc music player.
        self.vlc_player = vlc.MediaPlayer()

    # Function serving as the interface for user to use a music player.
    def start(self):

        # Try to create a service instance.
        self.create_service()

        # Try to find the music folder in google drive.
        self.find_music_folder()

        # Start the application logic.
        self.current_menu_name = "main_menu"
        while not self.is_application_quit:

            if self.current_menu_name == "main_menu":
                self.show_main_menu()
            elif self.current_menu_name == "music_menu":
                self.show_music_menu()
            elif self.current_menu_name == "playlist_menu":
                self.show_playlist_menu()

    # Function generating a service instance for using google api.
    def create_service(self):
        
        # Create the folder "tokens" if it's not existed.
        if os.path.exists("../tokens") == False:
            os.system("mkdir ../tokens")

        # Specify the target pickle file.
        # The pickle file records the user's access tokens and refresh tokens.
        # The pickle file is created when the authorization flow completes for the first time.
        pickle_file = "../tokens/token.pickle"

        # Check whether the pickle file exists or not.
        credential = None
        if os.path.exists(pickle_file):
            with open(pickle_file, "rb") as token:
                credential = pickle.load(token)

        # If the access token is expired, request a new one from google authorization server.
        # If there are no credential, create a new flow and start a local web server to ask the user for login.
        # Save the new credential for next run.
        if not credential or not credential.valid:
            if credential and credential.expired and credential.refresh_token:
                credential.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.client_secret_file, self.scopes)
                credential = flow.run_local_server(port=0)
            with open(pickle_file, "wb") as token:
                pickle.dump(credential, token)

        # Construct an instance for interacting with the API.
        try:
            self.service_instance = build(self.api_name, self.api_version, credentials=credential)
            print("the service instance is created successfully...")
        except Exception as e:
            print(e)
            print("Error: Fail to create a service instance.")
            sys.exit(1)

    # Function for searching the music folder in google drive.
    def find_music_folder(self):

        # Create a new query.
        # The defualt music folder is named "Music".
        query = "name = '{}'".format(self.music_folder_name)

        # Query google drive.
        response = self.service_instance.files().list(q=query).execute()
        files = response.get("files")
        next_page_token = response.get("nextPageToken")
        while next_page_token:
            response = self.service_instance.files().list(q=query).execute()
            files.extend(response.get("files"))
            next_page_token = response.get("nextPageToken")

        # Keep the folder ID if the music folder is found.
        self.music_folder_id = None
        for f in files:
            if f["name"] == self.music_folder_name and f["mimeType"] == "application/vnd.google-apps.folder":
                self.music_folder_id = f["id"]
                print("the music folder on google drive is found...")
                print("enjoy your music...\n")
                break
        if self.music_folder_id == None:
            print("Error: Please provide the correct name for your music folder.")
            sys.exit(1)

    # Function for showing the main menu.
    def show_main_menu(self):

        # Set the entries and the title for the main menu.
        menu_entries = ["play a song", "play a playlist", "quit"]
        menu_title = "welcome to my-music-player:"

        # Create the main menu.
        self.current_menu = TerminalMenu(menu_entries, title=menu_title)
        self.selected_index = self.current_menu.show()

        # Behave differently according to the entry selected by the user.
        if self.selected_index == 0:
            self.current_menu_name = "music_menu"
        elif self.selected_index == 1:
            self.current_menu_name = "playlist_menu"
        elif self.selected_index == 2:
            self.is_application_quit = True
            print("thanks for using my-music-player, see you again...")

    # Function for showing the playlist menu.
    def show_playlist_menu(self):

        # Initialize the folder id as the id of the root folder.
        music_folder_id = self.music_folder_id
        
        # Find all playlists and music.
        # Reset "self.all_music" and "self.all_playlist" before calling "self.get_all_music()".
        self.all_music, self.all_playlist = {}, {}
        self.get_all_music(music_folder_id=self.music_folder_id)
        
        # Set the entries and the title for the playlist menu.
        menu_entries = list(self.all_playlist.keys())
        menu_entries.insert(0, "return to main menu")
        menu_title = "here are all your playlists (select \"return to main menu\" to return): "
        
        # Create the playlist menu.
        self.current_menu = TerminalMenu(menu_entries, title=menu_title)
        self.selected_index = self.current_menu.show()
        
        # Behave differently according to the entry selected by the user.
        if self.selected_index == 0:
            self.current_menu_name = "main_menu"
        else:

            # Get all songs under the selected playlist.
            # Reset "self.all_music" and "self.all_playlist" before calling "self.get_all_music()".
            playlist_id = self.all_playlist[menu_entries[self.selected_index]]
            self.all_music, self.all_playlist = {}, {}
            self.get_all_music(music_folder_id=playlist_id)

            # Play each song sequentially.
            for file_name in list(self.all_music.keys()):

                # Download the music.
                self.download_music(self.all_music[file_name], file_name)
            
                # Play the music.
                print("start playing ({})...\n".format(file_name))
                if self.vlc_player.is_playing():
                    self.vlc_player.stop()
                self.vlc_player.set_media(vlc.Media("../downloads/" + file_name))
                self.vlc_player.play()

    # Function for showing the music menu.
    def show_music_menu(self):

        # Initialize the folder id as the id of the root folder.
        music_folder_id = self.music_folder_id

        # Find all playlists and music.
        # Reset "self.all_music" and "self.all_playlist" before calling "self.get_all_music()".
        self.all_music, self.all_playlist = {}, {}
        self.get_all_music(music_folder_id=self.music_folder_id)

        # Set the entries and the title for the music menu.
        menu_entries = list(self.all_music.keys())
        menu_entries.insert(0, "return to main menu")
        menu_title = "here are all your songs (select \"return to main menu\" to return): "
       
        # Create the music menu.
        self.current_menu = TerminalMenu(menu_entries, title=menu_title)
        self.selected_index = self.current_menu.show()
        
        # Behave differently according to the entry selected by the user.
        if self.selected_index == 0:
            self.current_menu_name = "main_menu"
        else:

            # Download the music.
            file_name = menu_entries[self.selected_index]
            self.download_music(self.all_music[file_name], file_name)

            # Play the music.
            print("start playing ({})...\n".format(file_name))
            if self.vlc_player.is_playing():
                self.vlc_player.stop()
            self.vlc_player.set_media(vlc.Media("../downloads/" + file_name))
            self.vlc_player.play()

    # Function for recursively searching to find all music and playlists.
    def get_all_music(self, music_folder_id):

        # Create a new query.
        query = "parents = '{}'".format(music_folder_id)

        # Query google drive.
        response = self.service_instance.files().list(q=query).execute()
        files = response.get("files")
        next_page_token = response.get("nextPageToken")
        while next_page_token:
            response = self.service_instance.files().list(q=query).execute()
            files.extend(response.get("files"))
            next_page_token = response.get("nextPageToken")

        # Record music and playlist as dictionary respectively.
        # If there are sub-directory, search the folders recursively.
        for f in files:
            if f["mimeType"] == "application/vnd.google-apps.folder":
                self.all_playlist[f["name"]] = f["id"]
                self.get_all_music(f["id"])
            else:
                self.all_music[f["name"]] = f["id"]

    # Function for downloading music from google drive.
    def download_music(self, file_id, file_name):

        # Create a new request.
        request = self.service_instance.files().get_media(fileId=file_id)

        # Create a downloader.
        self.file_stream = io.BytesIO()
        self.downloader = MediaIoBaseDownload(fd=self.file_stream, request=request)

        # Download the file.
        done = False
        while not done:
            status, done = self.downloader.next_chunk()

        # Change the stream position and save the downloaded file locally.
        # If the "downloads" folder isn't existed, create it first.
        self.file_stream.seek(0)
        if os.path.exists("../downloads") == False:
            os.system("mkdir ../downloads")
        with open(os.path.join("../downloads", file_name), "wb") as f:
            f.write(self.file_stream.read())
        print("download successfully ({})...".format(file_name))

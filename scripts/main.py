import sys
from create_service import create_service
from download_file import download_file
from search_google_drive import find_music_folder, get_all_music

# Set information for creating a service instance.
client_secret_file = "../credentials/client_secret.json"
api_name, api_version = "drive", "v3"
scopes = ["https://www.googleapis.com/auth/drive"]

# Create a service instance.
service_instance = create_service(client_secret_file, api_name, api_version, scopes)
if service_instance == None:
    print("Error: Fail to create a service instance.")
    sys.exit(1)
else:
    print("The service instance is created successfully...")

# Search for the music folder in google drive.
music_folder_ID = find_music_folder(service_instance)
if music_folder_ID == None:
    print("Error: Please name your music folder \"Music\" on google drive.")
    sys.exit(1)
else:
    print("The music folder on google drive is found...")

# List all music in the music folder.
# The key-value pairs in dictionaries are (music_name: music_id) and (sub-directory_name: sub-directory_id) respectively.
print("Here are all your music...\n")
all_subdirectory, all_music = {}, {}
get_all_music(service_instance, music_folder_ID, all_subdirectory, all_music)

# Enter the music name for downloading.
music_name = input("Enter the music name for downloading: ")
download_file(service_instance, all_music[music_name], music_name)

'''
file_ids = ["1YUM5L2dYXC3kVa-Y3X3jldHbrcojxHzf", "19LzH9RwbipJGva5p4MmuK4dW8yaTP009"]
file_names = ["Mai Kuraki - Always.mp3", "Mai Kuraki - Your Best Friend.mp3"]
for file_id, file_name in zip(file_ids, file_names):
    download_file(service_instance, file_id, file_name)
'''


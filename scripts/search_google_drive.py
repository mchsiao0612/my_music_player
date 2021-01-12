def find_music_folder(service_instance):

    # Create a new query.
    # The music folder in google drive must be named "Music".
    music_folder_name = "Music"
    query = "name = '{}'".format(music_folder_name)

    # Query google drive.
    response = service_instance.files().list(q=query).execute()
    files = response.get("files")
    next_page_token = response.get("nextPageToken")
    while next_page_token:
        response = service_instance.files().list(q=query).execute()
        files.extend(response.get("files"))
        next_page_token = response.get("nextPageToken")

    # Return the folder ID if the music folder is found.
    for f in files:
        if f["name"] == music_folder_name and f["mimeType"] == "application/vnd.google-apps.folder":
            return f["id"]
    return None

def get_all_music(service_instance, music_folder_ID, all_subdirectory, all_music):

    # Create a new query.
    query = "parents = '{}'".format(music_folder_ID)

    # Query google drive.
    response = service_instance.files().list(q=query).execute()
    files = response.get("files")
    next_page_token = response.get("nextPageToken")
    while next_page_token:
        response = service_instance.files().list(q=query).execute()
        files.extend(response.get("files"))
        next_page_token = response.get("nextPageToken")

    # If there are sub-directory, search the folders recursively.
    # Collect all music and sub-directory as dictionaries.
    for f in files:
        if f["mimeType"] == "application/vnd.google-apps.folder":
            all_subdirectory[f["name"]] = f["id"]
            print("folder: {}".format(f["name"]))
            get_all_music(service_instance, f["id"], all_subdirectory, all_music)
            print()
        else:
            all_music[f["name"]] = f["id"]
            print("- music: {}".format(f["name"]))


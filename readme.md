## Introduction
This is a command-line music player which accessing the music stored in google drive through google drive API. The interactive user interface is implemented with python [simple-term-menu](https://pypi.org/project/simple-term-menu/).

## Organization of Folders
The files are organized in folders as following:
- **scripts**: containing all python scripts.
- **credentials**: containing the credentials file named "client_secret.json".
- **tokens**: containing the token file named "token.pickle".
- **downloads**: containing the downloaded files during execution.

## Usage
1. Download the credential file from [Google Cloud Platform](https://console.cloud.google.com/).
2. Rename the credential file as **"client_secret.json"**, and put it in the **"credentials"** folder.
3. Prepare the .mp3 files in google drive, naming the root music folder **"Music"**.
4. Users can put their music into several playlists by creating sub-folders under the **"Music"** folder in google drive:
   ```
   Music (the root folder)
   |- playlist 1
        |- song A
        |- song B
        |- song C
   |- playlist 2
        |- song D
        |- song E
   ```
5. Move into the **"scripts"** folder, and run the **"main.py"** script.
    ```
    > cd scripts
    > python3 main.py
    ```
6. If this is the first time executing the script, a window will pop out in your browser. Allow the application to access your google drive for using this music application.
7. If this is not the first time executing the script, a token file named **"token.pickle"** has been saved in the **tokens** folder when the authentication flow completes for the first time, and the window of browser will not pop out this time.
8. After authenticating successfully, the program will try to create a service instance for using google drive API, and it will try to find the **"Music"** folder in your google drive. 
9. After the music folder is found, the main menu will shown in command line. Move the cursor to select a music or a playlist.
    ```
    > python3 main.py
    the service instance is created successfully...
    the music folder on google drive is found...
    enjoy your music...

    main menu:
    > play a song
      play a playlist
      exit
    ```
10. The program will download the music before playing it out loud, and the downloaded music will be removed from your computer automatically when you choose **"exit"** in the main menu.

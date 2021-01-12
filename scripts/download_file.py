import os
import io
from googleapiclient.http import MediaIoBaseDownload

def download_file(service_instance, file_id, file_name):

    # Create a new request.
    request = service_instance.files().get_media(fileId=file_id)

    # Create a downloader.
    file_stream = io.BytesIO()
    downloader = MediaIoBaseDownload(fd=file_stream, request=request)

    # Download the file.
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print("Downlaod progress ({}): {} %...".format(file_name, status.progress() * 100))

    # Change the stream position and save the downloaded file locally.
    # If the "downloads" folder isn't existed, create it first.
    file_stream.seek(0)
    if os.path.exists("../downloads") == False:
        os.system("mkdir ../downloads")
    with open(os.path.join("../downloads", file_name), "wb") as f:
        f.write(file_stream.read())
    print("Download successfully ({})...".format(file_name))

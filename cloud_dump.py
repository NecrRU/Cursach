from pydrive.drive import GoogleDrive 
from pydrive.auth import GoogleAuth 
import os 

def on_drive(file_name):
    gauth = GoogleAuth() 
    gauth.LocalWebserverAuth()

    drive = GoogleDrive(gauth)
    try:
        drive = GoogleDrive(gauth)
        my_file = drive.CreateFile({'title':f'{file_name}'})
        my_file.SetContentFile(file_name)
        my_file.Upload()
        return "sucsess"
    except Exception as ex:
        return "Error"
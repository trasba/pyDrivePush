## Simple Python module to upload files to Google Drive
# Needs a file 'client_secrets.json' in the directory 
# The file can be obtained from https://console.developers.google.com/ 
# under APIs&Auth/Credentials/Create Client ID for native application

import os
import sys #for arguments from commandline
import string #for split function
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

if (len(sys.argv) < 2):
  print "Expecting at least 1 argument -> exiting"
  sys.exit()

def login():
    global gauth, drive
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication
    drive = GoogleDrive(gauth) # Create GoogleDrive instance with authenticated GoogleAuth instance

def find_folders(fldname):
    file_list = drive.ListFile({
        'q': "mimeType contains 'application/vnd.google-apps.folder' and trashed=false"}).GetList()
    return file_list

def upload_files_to_folder(fname, folder):
        nfile = drive.CreateFile({'title':os.path.basename(fname), 'parents':[{u'id': folder[0]['id']}]})
        nfile.SetContentFile(fname)
        nfile.Upload() 

def find_files(filename, parentfid):
    file_list = drive.ListFile({
        'q': "title = '" + filename  + "' and '" + parentfid + "' in parents and trashed=false"}).GetList()
    return file_list

login()
folder = find_folders('kapi1-scan')
elements = string.split(sys.argv[1], '/')
intbefore = len(find_files(elements[len(elements)-1], folder[0]['id']))
upload_files_to_folder(sys.argv[1],folder)
intafter = len(find_files(elements[len(elements)-1], folder[0]['id']))
if (intafter != intbefore + 1):
  print "Upload failed we don't know what happened -> exiting"
  sys.exit()

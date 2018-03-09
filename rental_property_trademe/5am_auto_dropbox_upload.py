import sys
import datetime

import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

DROPBOX_TOKEN = 'BF-D66g71KMAAAAAAAANDCNDw15kKRhSKoMgmu3Tso0wfAj1Db1U0pd9PwzaMpKX'

FILE_NAME = "fast_" + datetime.datetime.now().strftime("%Y_%m_%d")+"_05.csv"

LOCAL_PATH = 'E:/web_scraping/raw_selenium_scraper/'

UPLOAD_PATH = '/team - share/Projects/Trademe VW Assessment/data/raw/'

# dbx = dropbox.Dropbox(DROPBOX_TOKEN)

# Uploads contents of LOCALFILE to Dropbox
def upload(file_name, local_path, upload_to_path):
    local_file_path = local_path + file_name
    upload_file_path = UPLOAD_PATH + FILE_NAME

    with open(local_file_path, 'rb') as f:
        # We use WriteMode=overwrite to make sure that the settings in the file
        # are changed on upload
        print("Uploading " + local_file_path + " to Dropbox as " + upload_file_path + "...")
        # print(f.read())
        try:
            dbx.files_upload(f.read(), upload_file_path, mode=WriteMode('overwrite'))
        except ApiError as err:
            # This checks for the specific error where a user doesn't have
            # enough Dropbox space quota to upload this file
            if (err.error.is_path() and
                    err.error.get_path().reason.is_insufficient_space()):
                sys.exit("ERROR: Cannot back up; insufficient space.")
            elif err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()

if __name__ == '__main__':
    # Check for an access token
    if (len(DROPBOX_TOKEN) == 0):
        sys.exit("ERROR: Looks like you didn't add your access token. "
            "Open up backup-and-restore-example.py in a text editor and "
            "paste in your token in line 14.")

    # Create an instance of a Dropbox class, which can make requests to the API.
    print("Creating a Dropbox object...")
    dbx = dropbox.Dropbox(DROPBOX_TOKEN)

    # Check that the access token is valid
    try:
        dbx.users_get_current_account()
    except AuthError as err:
        sys.exit("ERROR: Invalid access token; try re-generating an "
            "access token from the app console on the web.")

    # Create a backup of the current settings file
    upload(FILE_NAME, LOCAL_PATH, UPLOAD_PATH)

    print("Done!")

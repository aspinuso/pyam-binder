import dropbox




 
def uploadToDrop(source,destination,token):
    dbx = dropbox.Dropbox(token)
    with open(source, 'rb') as f:
      # We use WriteMode=overwrite to make sure that the settings in the file
      # are changed on upload
        print("Uploading  to Dropbox as " + destination + "...")
        try:
            response = dbx.files_upload(f.read(), destination, mode=dropbox.files.WriteMode.overwrite)
        except dropbox.exceptions.ApiError as err:
            # This checks for the specific error where a user doesn't have
            # enough Dropbox space quota to upload this file
            if (err.error.is_path() and err.error.get_path().error.is_insufficient_space()):
                sys.exit("ERROR: Cannot back up; insufficient space.")
            elif err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()
        print("Uploaded completed ")
        shared_link_metadata = dbx.sharing_create_shared_link(destination)
         
        return response,shared_link_metadata.url+"&raw=1"
# Data documentation

### Set up
To use data API, it is necessary to edd `.env` file into **local** repository with environment variables, such as `AWS_ACCESS_KEY`
and `AWS_SECRET_ACCESS_KEY`

## Methods

---

- ### `create_client`
Creates and returns S3 client (or resource), which can be used for remote database control. If something is wrong,
raises ConnectionException
---

- ### `upload_file`
Uploads local file to remote S3 database.

`path: str` - a path to local file

`key: str` - a key for file to be saved in remote S3 database (so the file is uploaded under this key)

---

- ### `get_bucket_size`
Returns the amount of data in database in **Mbytes**

---

- ### upload_files_from_folder

Uploads **all** files from the given folder until bucket is not full. 
If bucket size is more than allowed limits, than uploads nothing.

`path: str` - a path to the folder

`keys: list[str]` - list of keys, under which the files are saved in database. If it is not specified, then files are saved
under their local names

`allowed_size_in_mb: int = 4608` - allowed database size (the size of all elements in database).

---

- ### `get_file`

Returns a file from database by a given key in `StreamingBody` format.

`key: str` - a key under which the file is saved in database

--- 

- ### `get_and_save_files`

Saves file (or files) from database by a given key. 

`keys: str | list[str]` - if keys are `str`, then only one file is downloaded (which is saved under this key in database).
If keys are `list`, then all files which are saved in database under these keys will be downloaded. 
In this case the path to folder should be provided, and each file is downloaded under its key.

`path_to_save: str` - a path under which the file will be downloaded. If keys are `list`, then `path_to_save` should be a path 
to folder.

---









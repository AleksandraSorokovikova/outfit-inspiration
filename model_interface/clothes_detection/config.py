import os

dev_path = "../files/"
prod_path = "../temp_files/"

env = os.getenv("config", "dev")
if env == "dev":
    base_path = dev_path
else:
    base_path = prod_path

file_path_in_drive = "/content/drive/MyDrive/clothes.zip"
local_download_path = "/content/datasets/"
source_directory = "/content/yolov5/runs/train/exp"
destination_directory = "/content/drive/MyDrive/outrfit_insp"

model_name = "yolov5s.pt"
model_path = f"{base_path}yolov5s.pt"
annotations_file = f"{base_path}annotation.csv"
img_name = "pinterest/"
img_dir = f"{base_path}pinterest/"
segments_file_path = f"{base_path}segments_file.csv"
segments_file_name = "segments_file.csv"

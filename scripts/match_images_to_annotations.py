import os
import pandas as pd
import pdb
import numpy as np

images_path = os.path.join(os.path.expanduser("~"), ".skyimages", "folsom", "images")
annotation_path = os.path.join(
    os.path.expanduser("~"),
    ".skyimages",
    "folsom",
    "annotations",
    "Folsom_irradiance.csv",
)

df_annotations = pd.read_csv(annotation_path)
df_annotations["timeStamp"] = pd.to_datetime(df_annotations["timeStamp"])
df_annotations["image"] = np.nan


images_list = []
for path, subfolder, files in os.walk(images_path):
    print(path)
    for name in files:
        image_path = os.path.join(path, name).split(".skyimages\\")[1]
        date_string = (
            name.split(".")[0].split("_")[0] + name.split(".")[0].split("_")[1]
        )
        image_date = pd.Timestamp(date_string).floor("Min")
        df_indexes = df_annotations.loc[df_annotations["timeStamp"] == image_date]
        if not df_indexes.empty:
            index = df_indexes.index[0]
            df_annotations.at[index, "image"] = image_path

df_annotations.to_csv(
    os.path.join(
        os.path.expanduser("~"),
        ".skyimages",
        "folsom",
        "annotations",
        "Folsom_irradiance_edited.csv",
    )
)

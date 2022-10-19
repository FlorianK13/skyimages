import pandas as pd
import numpy as np
import os
import pdb


images_path = os.path.join(os.path.expanduser("~"), ".skyimages", "folsom", "images")
annotation_path = os.path.join(
    os.path.expanduser("~"),
    ".skyimages",
    "folsom",
    "annotations",
    "Folsom_irradiance_edited.csv",
)

annotation_df = pd.read_csv(annotation_path)

for index, row in annotation_df.iterrows():
    if row["image"] is not np.nan:
        pdb.set_trace()

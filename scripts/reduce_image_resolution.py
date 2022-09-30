from PIL import Image
import os
import numpy as np
import pdb
import pickle

pickle_process = False
images_to_folder_process = True


year = 2015
resolution = 128
month_list = [
    "12",
]  # ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

path = os.path.join(
    os.path.expanduser("~"),
    "Daten",
    "Pedro_SkyImages",
    f"Folsom_sky_images_{year}",
    str(year),
)

save_path = os.path.join(
    os.path.expanduser("~"),
    "Daten",
    "Pedro_SkyImages",
    "Reduced",
    str(resolution),
    str(year),
)


if images_to_folder_process:
    for month in month_list:
        for day in os.listdir(os.path.join(path, month)):
            print(f"{month}-{day}")

            folder_day_path = os.path.join(path, month, day)
            save_day_path = os.path.join(save_path, month, day)

            if not os.path.isdir(folder_day_path):
                continue
            if not os.path.exists(save_day_path):
                os.makedirs(save_day_path)

            for file in os.listdir(folder_day_path):
                filepath = os.path.join(folder_day_path, file)
                file_savepath = os.path.join(save_day_path, f"{year}_res{file}")
                try:
                    image = Image.open(filepath)
                    resized_image = image.resize((resolution, resolution))
                    resized_image.save(file_savepath)
                except OSError:
                    print(f"OSError: {file}")


if pickle_process:

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for month in os.listdir(path):
        monthly_dict = {}

        for day in os.listdir(os.path.join(path, month)):

            folder_day_path = os.path.join(path, month, day)

            if not os.path.isdir(folder_day_path):
                continue

            images_per_day = len(os.listdir(folder_day_path))
            daily_array = np.zeros((images_per_day, resolution, resolution, 3))

            for index, file in enumerate(os.listdir(folder_day_path)):
                filepath = os.path.join(folder_day_path, file)
                image = Image.open(filepath)
                resized_image = image.resize((resolution, resolution))
                image_array = np.array(resized_image)
                daily_array[index] = image_array

            monthly_dict[f"{year}{month}{day}"] = daily_array

        pickle_savepath = os.path.join(save_path, f"{year}{month}.pickle")
        with open(pickle_savepath, "wb") as file:
            pickle.dump(monthly_dict, file, protocol=pickle.HIGHEST_PROTOCOL)

import os
import shutil
from shutil import Error


def get_stored_dir():
    return "D:\\apk_pure\\download"


if __name__ == "__main__":
    for file in os.listdir(get_stored_dir()):
        if file.endswith(".apk"):
            app_name = file.split('.xapk')[0].split("_")[0]
            for _ in os.listdir(get_stored_dir()):
                if _.endswith(".xapk") and app_name in _:
                    target_path = os.path.join(get_stored_dir(), app_name)
                    if not os.path.exists(target_path):
                        os.mkdir(target_path)
                        shutil.move(os.path.join(get_stored_dir(), file), target_path)
                        shutil.move(os.path.join(get_stored_dir(), _), target_path)
                        break

import os
import shutil
from collections import Counter


def get_stored_dir():
    return "D:\\apk_pure\\download"


def get_result_dir():
    return "D:\\apk_pure\\t"


def merge_apk_file():
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


def move_apk_right_vision():
    for file in os.listdir(get_stored_dir()):
        file = os.path.join(get_stored_dir(), file)
        if os.path.isdir(file):
            apk_vision = ""
            xapk_vision = ""
            for _ in os.listdir(file):
                file_name = _
                _ = os.path.join(os.path.join(get_stored_dir(), file, _))
                if os.path.isfile(_):
                    if _.endswith(".apk"):
                        apk_vision = file_name.split("_")[1]
                    elif _.endswith(".xapk"):
                        xapk_vision = file_name.split("_")[1]
            if apk_vision != xapk_vision:
                app_name = file.replace(get_stored_dir() + "\\", "")
                for _ in os.listdir(get_stored_dir()):
                    _ = os.path.join(get_stored_dir(), _)
                    if os.path.isfile(_):
                        if app_name in _:
                            if _.endswith(".apk"):
                                if _.replace(get_stored_dir(), "").split("_")[1] == xapk_vision:
                                    print("--------------------")
                                    print(_, file)
                                    print("--------------------")
                                    shutil.move(_, file)
                                    print(_.split("_")[1])
                            elif _.endswith(".xapk"):
                                if _.replace(get_stored_dir(), "").split("_")[1] == apk_vision:
                                    print("--------------------")
                                    print(_, file)
                                    print("--------------------")
                                    shutil.move(_, file)


def remove_diff_vision():
    for file in os.listdir(get_stored_dir()):
        file = os.path.join(get_stored_dir(), file)
        if os.path.isdir(file):
            if len(os.listdir(file)) > 2:
                visions = []
                for _ in os.listdir(file):
                    visions.append(_.split("_")[1])
                print(visions)
                d = dict(Counter(visions))
                for i in [key for key, value in d.items() if value == 1]:
                    for _ in os.listdir(file):
                        if i in _:
                            print("remove " + os.path.join(file, _))
                            os.remove(os.path.join(file, _))


def check_version():
    for file in os.listdir(get_stored_dir()):
        file = os.path.join(get_stored_dir(), file)
        if os.path.isdir(file):
            apk_vision = ""
            xapk_vision = ""
            for _ in os.listdir(file):
                file_name = _
                _ = os.path.join(os.path.join(get_stored_dir(), file, _))
                if os.path.isfile(_):
                    if _.endswith(".apk"):
                        apk_vision = file_name.split("_")[1]
                    elif _.endswith(".xapk"):
                        xapk_vision = file_name.split("_")[1]
            if apk_vision == xapk_vision:
                print(file)
                print(file.replace(get_stored_dir(), get_result_dir()))
                shutil.move(file, file.replace(get_stored_dir(), get_result_dir()))


if __name__ == "__main__":
    move_apk_right_vision()
    remove_diff_vision()
    check_version()

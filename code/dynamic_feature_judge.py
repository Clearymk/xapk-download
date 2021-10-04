import zipfile
import os


def read_file_in_xapk(file_path):
    target_file = []
    with zipfile.ZipFile(file_path, 'r') as xapk_file:
        for apk_file in xapk_file.namelist():
            if apk_file.endswith("apk") and "config" not in apk_file:
                target_file.append(apk_file)
    if len(target_file) > 1:
        print(target_file)
        return True
    return False


if __name__ == "__main__":
    download_path = "F:\\download"

    for xapk_file in os.listdir(download_path):
        if not xapk_file.endswith("xapk"):
            continue
        xapk_file_path = os.path.join(download_path, xapk_file)
        if read_file_in_xapk(xapk_file_path):
            print(xapk_file_path)
            print("------------------------")

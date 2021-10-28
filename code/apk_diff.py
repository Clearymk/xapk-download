import os

tasks = []


def get_stored_path():
    return "D:\\apk_pure\\result"


def run_jar(apk_1, apk_2):
    os.chdir("D:\\apk_pure")
    command = "java -jar SimiDroid.jar %s %s" % (apk_1, apk_2)
    print(os.popen(command).read())


def get_task():
    for file in os.listdir(get_stored_path()):
        file = os.path.join(get_stored_path(), file)
        if os.path.isdir(file):
            task = []
            for _ in os.listdir(file):
                _ = os.path.join(file, _)
                if _.endswith(".apk"):
                    task.append(_)
            tasks.append(task)


if __name__ == "__main__":
    # for file in os.listdir(get_stored_path()):
    #     file = os.path.join(get_stored_path(), file)
    #     if os.path.isdir(file):
    #         list_file = os.listdir(file)
    #         if len(list_file) > 3:
    #             print(len(list_file))
    #             print(file)
    #             print(list_file)
    #             print("----------------------")
    #
    # for file in os.listdir(get_stored_path()):
    #     file = os.path.join(get_stored_path(), file)
    #     if os.path.isdir(file):
    #         list_file = os.listdir(file)
    #         for _ in list_file:
    #             _ = os.path.join(file, _)
    #             os.rename(_, _.replace(" ", "_"))

    get_task()
    current_task = ""
    flag = False
    for task in tasks:
        if current_task in task:
            flag = True

        if flag:
            run_jar(task[0], task[1])

import os
from datetime import datetime


def move_file(source, destination):
    if not os.path.exists(destination):
        os.rename(source, destination)


def path_join(path, join):
    new_path = os.path.join(os.path.sep, path, join)
    return new_path


def create_folder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def is_image(file):
    return ".jpg" in file or ".jpeg" in file or ".met" in file or ".nar" in file or ".png" in file


def is_movie(file):
    return ".mp4" in file or ".avi" in file or ".3gp" in file or ".rem" in file


def is_ignored(file):
    return ".ini" in file


def main():
    source = "c:\onedrive\Imagens\Imagens da Câmera"

    files = os.listdir(source)

    for cont in range(0, len(files)):
        file_analise(files[cont], source)


def file_analise(file, source):
    destination = "c:\onedrive"
    absolute_source = os.path.join(os.path.sep, source, file)
    year = str(datetime.fromtimestamp(os.path.getctime(absolute_source)).year)
    month = "{0:0>2}".format(str(datetime.fromtimestamp(os.path.getctime(absolute_source)).month))

    if is_ignored(file):
        return
    elif is_movie(file):
        destination = path_join(destination, "Vídeos")
    elif is_image(file):
        destination = path_join(destination, "Imagens")
    else:
        destination = path_join(destination, "Outros")

    if "IMG_" == file[0:4] or "VID_" == file[0:4]:
        year = file[4:8]
        month = file[8:10]
    elif "WP_" == file[0:3]:
        year = file[3:7]
        month = file[7:9]
    elif "Screenshot" == file[0:10]:
        destination = path_join(destination, "Capturas de tela")
    elif "WA" in file:
        year = file[4:8]
        month = file[8:10]
        destination = path_join(destination, "WhatsApp")
    elif "FB_I" == file[0:4]:
        destination = path_join(destination, "Imagens Salvas")
    else:
        destination = path_join(destination, "Outros")

    destination = path_join(destination, year)
    destination = path_join(destination, month)

    absolute_destination = path_join(destination, file)

    move_file(absolute_source, absolute_destination)


main()


import os
import multiprocessing
import re
import subprocess

from datetime import datetime


def available_cpu_count():
    """ Number of available virtual or physical CPUs on this system, i.e.
    user/real as output by time(1) when called with an optimally scaling
    userspace-only program"""

    # cpuset
    # cpuset may restrict the number of *available* processors
    try:
        m = re.search(r'(?m)^Cpus_allowed:\s*(.*)$',
                      open('/proc/self/status').read())
        if m:
            res = bin(int(m.group(1).replace(',', ''), 16)).count('1')
            if res > 0:
                return res
    except IOError:
        pass

    # Python 2.6+
    try:
        import multiprocessing
        return multiprocessing.cpu_count()
    except (ImportError, NotImplementedError):
        pass

    # https://github.com/giampaolo/psutil
    try:
        import psutil
        return psutil.cpu_count()   # psutil.NUM_CPUS on old versions
    except (ImportError, AttributeError):
        pass

    # POSIX
    try:
        res = int(os.sysconf('SC_NPROCESSORS_ONLN'))

        if res > 0:
            return res
    except (AttributeError, ValueError):
        pass

    # Windows
    try:
        res = int(os.environ['NUMBER_OF_PROCESSORS'])

        if res > 0:
            return res
    except (KeyError, ValueError):
        pass

    # jython
    try:
        from java.lang import Runtime
        runtime = Runtime.getRuntime()
        res = runtime.availableProcessors()
        if res > 0:
            return res
    except ImportError:
        pass

    # BSD
    try:
        sysctl = subprocess.Popen(['sysctl', '-n', 'hw.ncpu'],
                                  stdout=subprocess.PIPE)
        scStdout = sysctl.communicate()[0]
        res = int(scStdout)

        if res > 0:
            return res
    except (OSError, ValueError):
        pass

    # Linux
    try:
        res = open('/proc/cpuinfo').read().count('processor\t:')

        if res > 0:
            return res
    except IOError:
        pass

    # Solaris
    try:
        pseudoDevices = os.listdir('/devices/pseudo/')
        res = 0
        for pd in pseudoDevices:
            if re.match(r'^cpuid@[0-9]+$', pd):
                res += 1

        if res > 0:
            return res
    except OSError:
        pass

    # Other UNIXes (heuristic)
    try:
        try:
            dmesg = open('/var/run/dmesg.boot').read()
        except IOError:
            dmesgProcess = subprocess.Popen(['dmesg'], stdout=subprocess.PIPE)
            dmesg = dmesgProcess.communicate()[0]

        res = 0
        while '\ncpu' + str(res) + ':' in dmesg:
            res += 1

        if res > 0:
            return res
    except OSError:
        pass

    raise Exception('Can not determine number of CPUs on this system')


def file_analise(file, _source):
    destination = "d:\\onedrive"
    absolute_source = os.path.join(os.path.sep, _source, file)
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
    elif "Screenshot" == file[0:10] or "Captur" == file[0:6]:
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

    absolute_destination = path_join(destination, file, False)

    move_file(absolute_source, absolute_destination)


def move_file(origin, destination):
    if not os.path.exists(destination):
        os.rename(origin, destination)
        print(origin, " to ", destination)
    else:
        print(origin, " to ", destination, " already exists")


def path_join(path, join, create=True):
    new_path = os.path.join(os.path.sep, path, join)
    if create:
        create_folder(new_path)
    return new_path


def create_folder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def is_image(file):
    if ".jpg" in file:
        return True
    if ".jpeg" in file:
        return True
    if ".met" in file:
        return True
    if ".nar" in file:
        return True
    if ".png" in file:
        return True
    return False


def is_movie(file):
    if ".mp4" in file:
        return True
    if ".avi" in file:
        return True
    if ".3gp" in file:
        return True
    if ".rem" in file:
        return True
    return False


def is_ignored(file):
    if ".ini" in file:
        return True


if __name__ == '__main__':
    source = "d:\\onedrive\\Imagens\\Imagens da Câmera"

    files = os.listdir(source)
    processors = available_cpu_count()
    pool = multiprocessing.Pool(processors)

    for cont in range(0, len(files)):
        pool.apply_async(file_analise, (files[cont],), {'_source': source})

    pool.close()
    pool.join()


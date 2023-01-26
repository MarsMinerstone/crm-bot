import os
import subprocess
import sys
import time


def keyboard_interrupt_hook(exctype, value, traceback):
    """keyboard interrupt handler."""
    if exctype == KeyboardInterrupt:
        print("The process has been stopped")
    else:
        sys.__excepthook__(exctype, value, traceback)


sys.excepthook = keyboard_interrupt_hook


def pre_reloader():
    """accepting and validating arguments."""
    paths = sys.argv
    if len(paths) != 3:
        print(f"ArgumentsException: {len(paths) - 1} arguments was/were given, 2 needed.")
        return

    path_to_dir = paths[1]
    path_to_file = paths[2]

    if not os.path.isdir(path_to_dir):
        print(f"CutomArgumentException: first arguments must be correct dir path.")
        return

    if not os.path.isfile(path_to_file):
        print(f"CustomArgumentException: second arguments must be correct file path.")
        return

    reloader(file_filter(path_to_dir), path_to_file)


def file_filter(path_to_dir):
    dirs = os.listdir(path_to_dir)

    exclude = "/__pycache__ /venv /__init__.py /rebooter.py /base.db /.DS_Store /data"

    to_remove = []

    for fname in dirs:
        if fname not in exclude:
            if os.path.isdir(f"{path_to_dir}/{fname}"):
                _dirs = file_filter(f"{path_to_dir}/{fname}")
                dirs += _dirs
                to_remove.append(fname)
            elif "/" not in fname:
                dirs[dirs.index(fname)] = path_to_dir + \
                    "/" + dirs[dirs.index(fname)]
        else:
            to_remove.append(fname)

    for f in to_remove:
        dirs.remove(f)

    return dirs


def reloader(files: str, path_to_file: str):
    """process reloader."""
    p = subprocess.Popen(f"python3 {path_to_file}", shell=True)

    last_mtime = {}

    while 1:
        time.sleep(1)
        for fname in files:

            t = os.path.getmtime(fname)

            if last_mtime.get(fname):
                if last_mtime.get(fname) < t:
                    print(f"The file {fname} was changed. Restarting ...")
                    p.kill()
                    p = subprocess.Popen(f"python3 {path_to_file}", shell=True)
                    print("Process restarted.")

            last_mtime[fname] = t


def main():
    pre_reloader()


if __name__ == '__main__':
    main()

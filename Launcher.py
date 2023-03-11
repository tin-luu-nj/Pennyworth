import subprocess
import sys
import os
import errno

""" Sequence:
1. Check if Launcher is running
--2. Check if venv activate script is exist
--3. If venv is not exist, create it
--4. Activate venv
5. Check for new version of project
5. Check and Install requirement
6. Run Application
7. While Application is running, periodcally check for update
8. If update avaialbe, exit Application and restart Launcher

"""
from src import DEM
from generated.DTC import *
from src.pyAutoUpdate import check_for_update, update


def Launcher_repeat_prevent():
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    try:
        file_handle = os.open("Launcher.lock", flags)
    except OSError as e:
        if e.errno == errno.EEXIST:  # Failed as the file already exists.
            print("[ERROR] Launcher is running!\n")
            exit()
        else:  # Something unexpected went wrong so reraise the exception.
            raise
    else:  # No exception, so the file must have been created successfully.
        with os.fdopen(file_handle, "w") as file_obj:
            # Using `os.fdopen` converts the handle to an object that acts like a
            # regular Python file object, and the `with` context manager means the
            # file will be automatically closed when we're done with it.
            file_obj.write("Look, ma, I'm writing to a new file")


def Launcher_lock_release():
    file_path = "Launcher.lock"
    try:
        os.remove(file_path)
    except OSError as e:
        print("Error: %s : %s" % (file_path, e.strerror))


def run():
    os.system("python Application.py &")


def get_base_prefix_compat():
    """Get base/real prefix, or sys.prefix if there is none."""
    return (
        getattr(sys, "base_prefix", None)
        or getattr(sys, "real_prefix", None)
        or sys.prefix
    )


def in_virtualenv():
    return get_base_prefix_compat() != sys.prefix


def main():
    if in_virtualenv():
        check_for_update()
        if DEM.cleanup(DEM_EVENT_AUTOUPDATE_NEW_VERSION_AVAILABLE):
            update()
        run()
    else:
        print("[ERROR] Please activate venv!\n")


if "__main__" == __name__:
    Launcher_repeat_prevent()
    try:
        main()
    finally:
        Launcher_lock_release()

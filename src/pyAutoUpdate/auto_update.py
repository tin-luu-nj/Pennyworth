import subprocess
import sys

from generated.DTC import *
from src.pyAbstract.generic import DEM


def _git_get_current_branch():
    current_branch = subprocess.check_output(["git", "branch", "--show-current"])
    return current_branch.decode("utf-8")[:-1]


def _git_get_number_of_ahead_behind_commit():
    commit_number = subprocess.check_output(
        [
            "git",
            "rev-list",
            "--left-right",
            "--count",
            "master...remotes/Pennyworth/master",
        ]
    )
    return [int(i) for i in commit_number.decode("utf-8")[:-1].split("\t")]


def _git_fetch():
    subprocess.check_call(["git", "fetch"])


def _git_pull():
    subprocess.check_call(["git", "pull"])


def _install_requirement():
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
    )


def update():
    branch = _git_get_current_branch()
    if "master" == branch:
        _git_pull()
        _install_requirement()


def check_for_update():
    _git_fetch()
    commit_number = _git_get_number_of_ahead_behind_commit()
    if all([commit_number[0] > 0, commit_number[1] == 0]):
        DEM.set_event_status(DEM_EVENT_AUTOUPDATE_NEW_VERSION_AVAILABLE)

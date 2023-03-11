import subprocess
import sys

from generated.DTC import *
from src.pyAbstract.generic import DEM

from git.repo import Repo

repo = Repo("./")

def _git_get_current_branch():
    branch=repo.active_branch
    return branch.name

def _git_get_number_of_ahead_behind_commit():
    commits_behind = repo.iter_commits('master..origin/master')
    commits_ahead = repo.iter_commits('origin/master..master')
    count_behind = sum(1 for c in commits_behind)
    count_ahead = sum(1 for c in commits_ahead)
    return [count_behind, count_ahead]

def _git_fetch():
    repo.remotes.origin.fetch() 


def _git_pull():
    repo.remotes.origin.pull() 


def _git_reset():
    repo.git.reset('--hard')

def _install_requirement():
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
    )


def update():
    branch = _git_get_current_branch()
    if "master" == branch:
        _git_reset()
        _git_pull()
        _install_requirement()


def check_for_update():
    _git_fetch()
    commit_number = _git_get_number_of_ahead_behind_commit()
    if all([commit_number[0] > 0, commit_number[1] == 0]):
        DEM.set_event_status(DEM_EVENT_AUTOUPDATE_NEW_VERSION_AVAILABLE)

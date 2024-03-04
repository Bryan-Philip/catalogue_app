import os
from time import sleep
from git import Repo
import subprocess
import re

COMMITS_TO_PRINT = 5

def print_commit(commit):
    print('----')
    print(str(commit.hexsha))
    print("\"{}\" by {} ({})".format(commit.summary,
                                     commit.author.name,
                                     commit.author.email))
    print(str(commit.authored_datetime))
    print(str("count: {} and size: {}".format(commit.count(),
                                              commit.size)))

def print_repository(repo):
    print('Repo description: {}'.format(repo.description))
    print('Repo active branch is {}'.format(repo.active_branch))
    for remote in repo.remotes:
        print('Remote named "{}" with URL "{}"'.format(remote, remote.url))
    print('Last commit for repo is {}.'.format(str(repo.head.commit.hexsha)))

repo_path = "/Users/User/Desktop/catalogue_app"
repo = Repo(repo_path)

# Get Untracked Files
# print(repo.untracked_files)

# if __name__ == "__main__":
#     # check that the repository loaded correctly
#     if not repo.bare:
#         print('Repo at {} successfully loaded.'.format(repo_path))
#         print_repository(repo)
#         # create list of commits then print some of them to stdout
#         commits = list(repo.iter_commits('master'))[:COMMITS_TO_PRINT]
#         for commit in commits:
#             print(commit)
#             # print_commit(commit)
#             pass
#     else:
#         print('Could not load repository at {} :('.format(repo_path))

# repo_remote_url = 'https://github.com/Cypherjac/catalogue_app.git'

repo_remote_url = 'https://github.com/Yego001/brokerApp.git'

def COMMIT_HASH(source):
    if source == 'local':
        return str(repo.head.commit.hexsha)
    elif source == 'remote':
        process = subprocess.Popen(["git", "ls-remote", repo_remote_url], stdout=subprocess.PIPE)
        stdout, stderr = process.communicate()
        sha = re.split(r'\t+', stdout.decode('ascii'))[0]
        return sha

# def COMMIT_STATUS(commit):

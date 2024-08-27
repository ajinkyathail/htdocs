import os
import paramiko
import git
from pathlib import Path

# Configuration
FTP_HOST = os.getenv('FTP_HOST')
FTP_USER = os.getenv('FTP_USER')
FTP_PASSWORD = os.getenv('FTP_PASSWORD')
FTP_REMOTE_DIR = 'htdocs'
LOCAL_DIR = 'ftp_sync_temp'
GIT_REPO_DIR = '.'

# Initialize directories
Path(LOCAL_DIR).mkdir(parents=True, exist_ok=True)

# Connect to the FTP server
def ftp_sync():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(FTP_HOST, username=FTP_USER, password=FTP_PASSWORD)

    sftp = ssh.open_sftp()
    sftp.chdir(FTP_REMOTE_DIR)

    # Sync files from FTP to local directory
    for item in sftp.listdir_attr():
        remote_path = FTP_REMOTE_DIR + '/' + item.filename
        local_path = os.path.join(LOCAL_DIR, item.filename)

        if stat.S_ISDIR(item.st_mode):
            Path(local_path).mkdir(parents=True, exist_ok=True)
        else:
            sftp.get(remote_path, local_path)
    
    sftp.close()
    ssh.close()

# Sync local directory with Git repository
def git_sync():
    repo = git.Repo(GIT_REPO_DIR)
    repo.git.add(A=True)
    if repo.git.diff('HEAD', '--quiet'):
        print("No changes detected.")
    else:
        repo.index.commit("Sync from FTP server")
        origin = repo.remote(name='origin')
        origin.push()

def main():
    print("Syncing files from FTP server to local directory...")
    ftp_sync()
    print("Sync complete.")
    
    print("Syncing with Git repository...")
    git_sync()
    print("Git sync complete.")

if __name__ == '__main__':
    main()

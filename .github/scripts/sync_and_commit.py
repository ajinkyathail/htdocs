import os
import ftplib
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
    ftp = ftplib.FTP(FTP_HOST)
    ftp.login(user=FTP_USER, passwd=FTP_PASSWORD)
    ftp.cwd(FTP_REMOTE_DIR)

    def download_files(remote_dir, local_dir):
        os.makedirs(local_dir, exist_ok=True)
        ftp.cwd(remote_dir)
        for item in ftp.nlst():
            local_path = os.path.join(local_dir, item)
            if is_directory(item):
                download_files(item, local_path)
            else:
                with open(local_path, 'wb') as f:
                    ftp.retrbinary('RETR ' + item, f.write)

    def is_directory(name):
        try:
            ftp.cwd(name)
            return True
        except ftplib.error_perm:
            return False

    download_files(FTP_REMOTE_DIR, LOCAL_DIR)
    ftp.quit()

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

import os
import ftplib
import git
from pathlib import Path
from datetime import datetime

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
                # Check if the file needs to be downloaded
                if should_download(item, local_path):
                    print(f"Transferring file '{item}' to '{local_path}'")
                    with open(local_path, 'wb') as f:
                        ftp.retrbinary('RETR ' + item, f.write)

    def should_download(remote_file, local_path):
        """Check if a file should be downloaded based on its size or modification date."""
        try:
            remote_size = ftp.size(remote_file)
            remote_mtime = ftp.sendcmd(f"MDTM {remote_file}")[4:]
            remote_mtime = datetime.strptime(remote_mtime, "%Y%m%d%H%M%S")

            if os.path.exists(local_path):
                local_size = os.path.getsize(local_path)
                local_mtime = datetime.fromtimestamp(os.path.getmtime(local_path))

                if remote_size == local_size and remote_mtime <= local_mtime:
                    print(f"Skipping '{remote_file}' (no changes detected)")
                    return False

            return True

        except Exception as e:
            print(f"Error checking file '{remote_file}': {e}")
            return True

    def is_directory(name):
        """Check if the name is a directory on the FTP server."""
        current = ftp.pwd()
        try:
            ftp.cwd(name)
            ftp.cwd(current)
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

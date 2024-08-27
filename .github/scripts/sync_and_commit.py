from ftplib import FTP, error_perm
import os

# FTP connection details (use environment variables for safety)
FTP_HOST = os.getenv('FTP_HOST')
FTP_USER = os.getenv('FTP_USERNAME')
FTP_PASSWORD = os.getenv('FTP_PASSWORD')
FTP_REMOTE_DIR = 'htdocs'  # Set to the correct directory on the server
LOCAL_DIR = 'ftp_sync_temp'  # Directory to sync files locally

def download_files(remote_dir, local_dir):
    try:
        # Check if the remote directory exists
        ftp.cwd(remote_dir)
    except error_perm as e:
        print(f"Error: Cannot change directory to {remote_dir}. {e}")
        return

    os.makedirs(local_dir, exist_ok=True)
    file_list = ftp.nlst()

    for file_name in file_list:
        local_file = os.path.join(local_dir, file_name)
        if os.path.isdir(local_file):
            download_files(file_name, local_file)  # Recursively download subdirectories
        else:
            with open(local_file, 'wb') as f:
                ftp.retrbinary(f'RETR {file_name}', f.write)
                print(f"Downloaded: {file_name}")

def ftp_sync():
    global ftp
    ftp = FTP(FTP_HOST)
    ftp.login(FTP_USER, FTP_PASSWORD)
    
    print("Syncing files from FTP server to local directory...")
    download_files(FTP_REMOTE_DIR, LOCAL_DIR)
    ftp.quit()
    print("Sync complete.")

def main():
    ftp_sync()

if __name__ == "__main__":
    main()

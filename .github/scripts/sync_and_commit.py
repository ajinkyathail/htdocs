from ftplib import FTP
import os

FTP_HOST = os.getenv('FTP_HOST')
FTP_USER = os.getenv('FTP_USER')
FTP_PASSWORD = os.getenv('FTP_PASSWORD')
FTP_REMOTE_DIR = 'remote_directory'  # Replace with your actual remote directory
LOCAL_DIR = 'local_directory'  # Replace with your actual local directory

def download_files(ftp, remote_dir, local_dir):
    # Change to the remote directory
    try:
        ftp.cwd(remote_dir)
        os.makedirs(local_dir, exist_ok=True)
        print(f"Changed to directory: {remote_dir}")
    except Exception as e:
        print(f"Error changing directory to {remote_dir}: {e}")
        return

    file_list = ftp.nlst()  # Get the list of files

    for file_name in file_list:
        local_file = os.path.join(local_dir, file_name)

        try:
            if is_directory(ftp, file_name):
                # Recursively download subdirectory
                download_files(ftp, file_name, local_file)
            else:
                # Download file
                print(f"Downloading file: {file_name} to {local_file}")
                with open(local_file, 'wb') as f:
                    ftp.retrbinary(f'RETR {file_name}', f.write)
        except Exception as e:
            print(f"Error processing {file_name}: {e}")

    # Return to parent directory
    ftp.cwd('..')
    print(f"Returned to parent directory")

def is_directory(ftp, file_name):
    """Check if a file is a directory."""
    current = ftp.pwd()
    try:
        ftp.cwd(file_name)
        ftp.cwd(current)
        return True
    except Exception:
        return False

def ftp_sync():
    ftp = FTP(FTP_HOST)
    ftp.login(FTP_USER, FTP_PASSWORD)
    print("Successfully logged in to FTP server.")
    
    download_files(ftp, FTP_REMOTE_DIR, LOCAL_DIR)

    ftp.quit()

def main():
    ftp_sync()

if __name__ == "__main__":
    main()

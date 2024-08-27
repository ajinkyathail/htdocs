def download_files(ftp, remote_dir, local_dir):
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
                print(f"Entering directory: {file_name}")
                download_files(ftp, file_name, local_file)
            else:
                if should_download(ftp, file_name, local_file):
                    print(f"Downloading file: {file_name} to {local_file}")
                    with open(local_file, 'wb') as f:
                        ftp.retrbinary(f'RETR {file_name}', f.write)
                else:
                    print(f"File already up-to-date: {local_file}")
        except Exception as e:
            print(f"Error processing {file_name}: {e}")

    ftp.cwd('..')
    print(f"Returned to parent directory")


def should_download(ftp, file_name, local_file):
    """Check if a file should be downloaded based on modification date or size."""
    remote_size = ftp.size(file_name)
    remote_mdtm = ftp.sendcmd(f"MDTM {file_name}").split()[1]
    
    if os.path.exists(local_file):
        local_size = os.path.getsize(local_file)
        local_mtime = time.strftime('%Y%m%d%H%M%S', time.gmtime(os.path.getmtime(local_file)))

        if remote_size == local_size and remote_mdtm <= local_mtime:
            return False  # File is up-to-date
    return True  # File should be downloaded

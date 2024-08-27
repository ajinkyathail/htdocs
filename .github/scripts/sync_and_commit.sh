name: FTP to Git Sync

on:
  workflow_dispatch: # Allows manual trigger of the workflow

jobs:
  sync_ftp_to_git:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
        with:
          ref: main

      - name: Install lftp
        run: sudo apt-get install -y lftp

      - name: Make sync script executable
        run: chmod +x sync_and_commit.sh

      - name: Run sync script
        env:
          FTP_HOST: ${{ secrets.FTP_HOST }}
          FTP_USER: ${{ secrets.FTP_USERNAME }}
          FTP_PASSWORD: ${{ secrets.FTP_PASSWORD }}
          FTP_REMOTE_DIR: htdocs
        run: ./sync_and_commit.sh

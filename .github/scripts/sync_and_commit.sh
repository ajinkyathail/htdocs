#!/bin/bash
set -e

# Environment variables
FTP_HOST=${FTP_HOST}
FTP_USER=${FTP_USER}
FTP_PASSWORD=${FTP_PASSWORD}
FTP_REMOTE_DIR=${FTP_REMOTE_DIR}

# Directories
LOCAL_DIR="."
REMOTE_DIR="ftp_sync"

# Ensure local directory exists
mkdir -p $REMOTE_DIR

echo "Syncing files from FTP server to local directory..."

# Sync files from FTP to local directory
lftp -f "
open ftp://$FTP_USER:$FTP_PASSWORD@$FTP_HOST
mirror --continue --delete --verbose --only-newer --no-empty-dirs $FTP_REMOTE_DIR $REMOTE_DIR
bye
"

echo "Sync complete."

# Move synced files to the repository root
rsync -av --delete $REMOTE_DIR/ $LOCAL_DIR/

# Remove the temporary sync directory
rm -rf $REMOTE_DIR

echo "Checking for changes in the repository..."

# Configure Git
git config --local user.email "actions@github.com"
git config --local user.name "GitHub Actions"

# Check for changes
if git status --porcelain | grep -q .; then
  echo "Changes detected."
  git add --all
  git diff-index --quiet HEAD || git commit -m "Sync from FTP server"
  git push origin main
else
  echo "No changes detected."
fi

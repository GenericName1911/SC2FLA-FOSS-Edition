#!/bin/bash
#python stuff
python3 -m venv myenv
source myenv/bin/activate
python3 setup.py

#download the LATEST exe files 
OWNER="Daniil-SV"
REPO="ScDowngrade"

API_URL="https://api.github.com/repos/$OWNER/$REPO/releases/latest"
RELEASE_DATA=$(curl -s "$API_URL")
ASSET_URL=$(echo "$RELEASE_DATA" | grep "browser_download_url" | cut -d '"' -f 4 | head -n 1)
FILENAME=$(basename "$ASSET_URL")
echo "Downloading $FILENAME from $ASSET_URL"
curl -L -o "$FILENAME" "$ASSET_URL"

chmod +x $FILENAME
mv $FILENAME ./lib/$FILENAME

OWNER="Daniil-SV"
REPO="SCTX-Converter"

API_URL="https://api.github.com/repos/$OWNER/$REPO/releases/latest"
RELEASE_DATA=$(curl -s "$API_URL")
ASSET_URL=$(echo "$RELEASE_DATA" | grep "browser_download_url" | cut -d '"' -f 4 | sed -n 2p)
FILENAME=$(basename "$ASSET_URL")
echo "Downloading $FILENAME from $ASSET_URL"
curl -L -o "$FILENAME" "$ASSET_URL"

chmod +x $FILENAME
mv $FILENAME ./lib/$FILENAME

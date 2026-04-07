#! /usr/bin/env bash

export ZIP_NAME="project2"
export ZIP_DIR="zip/$ZIP_NAME"

rm -f $ZIP_NAME.zip
rm -rf $ZIP_DIR
mkdir -p $ZIP_DIR

# I believe this is everything we need
cp -r .devcontainer/ $ZIP_DIR/
cp -r .vscode/ $ZIP_DIR/
cp -r * $ZIP_DIR/

echo "Zipping..."
cd zip/
zip $ZIP_NAME.zip -r $ZIP_NAME
mv $ZIP_NAME.zip ..
cd ..
echo "Written to $ZIP_NAME.zip. Inspect $ZIP_DIR/ to confirm contents"
echo "Confirm contents before submitting!"

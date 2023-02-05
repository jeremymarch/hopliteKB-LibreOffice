#! /bin/sh
cp LICENSE src/LICENSE
cp README.md src/README.md
cd src
rm ../hoplitekb.oxt
rm -R py/__pycache__
rm .DS_Store
rm py/.DS_Store
zip -r ../hoplitekb.oxt *
cd ..
rm src/LICENSE
rm src/README.md

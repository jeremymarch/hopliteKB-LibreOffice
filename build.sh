#! /bin/sh
cp LICENSE src/LICENSE
cp README.md src/README.md
cd src
rm ../hoplitekb.oxt
zip -r ../hoplitekb.oxt *
cd ..
rm src/LICENSE
rm src/README.md

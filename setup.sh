#! /bin/sh

# Make sure npm has the packages
cd purdue-navigation-client && npm install

# Generate production code
npm run build

# Move build to above for flask to use
rm -rf ../build
mv build ../
cd ..

# Deploy 
gcloud app deploy app.yaml
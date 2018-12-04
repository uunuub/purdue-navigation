#! /bin/sh

cd purdue-navigation-client && npm run build

mv build ../ && cd ..

gcloud app deploy
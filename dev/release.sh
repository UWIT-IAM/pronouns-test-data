#!/usr/bin/env bash

VERSION="$1"
DATADIR=pronouns_test_data/data
BUCKET_NAME=uwit-iam-identity-static
UPLOAD_DIR="${BUCKET_NAME}/pronouns/test-data"

if test -z "${VERSION}"
then
  echo "No version specified. Please enter a version number or a patch level from:
  patch, minor, major."
  exit 1
fi

poetry version "${VERSION}"
VERSION="$(poetry version -s)"

cp "${DATADIR}/latest.csv" "${DATADIR}/${VERSION}.csv"
cp "${DATADIR}/latest.json" "${DATADIR}/${VERSION}.json"

gcloud auth login


gsutil cp pronouns_test_data/data/*.{csv,json} gs://${BUCKET_NAME}/pronouns/test-data/


#!/usr/bin/env bash

# This script is only to be used after the data in `latest.json` has been published
# to Identity Registry.

DATADIR=pronouns_test_data/data
BUCKET_NAME=uwit-iam-identity-static
UPLOAD_DIR="${BUCKET_NAME}/pronouns/test-data"
GCLOUD_PROJECT=uwit-mci-iam
VERSION=
CMD_PREFIX=
DRY_RUN=

while (( $# ))
do
  case "$1" in
    --dry-run)
      DRY_RUN=1
      CMD_PREFIX="echo [DRY RUN] "
      ;;
    --version|-v)
      shift
      VERSION="$1"
      ;;
  esac
  shift
done

if test -z "${VERSION}"
then
  echo "No version specified. Please enter a version number or a patch level from:
  patch, minor, major."
  exit 1
fi

if test -n "$(git status -s)"
then
  echo "Your git branch is dirty. I can't release a version that has no commit!"
  echo "Either add and commit your changes, or reset them, then try again."
  exit 1
fi

if test "$(git branch --show-current)" != 'main'
then
  echo "You are not on the \`main\` branch. I cannot tag this branch."
  exit 1
fi

echo "Authenticating you with the Google Cloud. Please follow any prompts."
$CMD_PREFIX gcloud auth login

echo "Ensuring Google cloud project set to ${GCLOUD_PROJECT}."
$CMD_PREFIX gcloud config set project ${GCLOUD_PROJECT}

poetry version "${VERSION}" 2>/dev/null
VERSION="$(poetry version -s 2>/dev/null)"

echo "Creating assets for version ${VERSION}"
JSON_ASSET="${DATADIR}/${VERSION}.json"
CSV_ASSET="${DATADIR}/${VERSION}.csv"
$CMD_PREFIX cp "${DATADIR}/latest.csv" "${CSV_ASSET}"
$CMD_PREFIX cp "${DATADIR}/latest.json" "${JSON_ASSET}"

$CMD_PREFIX git add pyproject.toml "${JSON_ASSET}" "${CSV_ASSET}"
$CMD_PREFIX git commit -m "Release version ${VERSION}"

echo "Copying assets to the storage bucket"
$CMD_PREFIX gsutil cp pronouns_test_data/data/*.{csv,json} gs://${BUCKET_NAME}/pronouns/test-data/

echo "Tagging commit as version ${VERSION}"
$CMD_PREFIX git tag -a "${VERSION}" -m "Release version ${VERSION}"
$CMD_PREFIX git push origin "${VERSION}"

if test -n "${DRY_RUN}"
then
  echo "Resetting local changes to pyproject.toml after dry run"
  git checkout -f pyproject.toml
fi

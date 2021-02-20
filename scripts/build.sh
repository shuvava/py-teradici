#!/bin/sh
#set root directory
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )/.." >/dev/null 2>&1 && pwd )"
cd "${DIR}"

# set common variables
set -a
[ -f .env ] && . .env
set +a
# set variables
IMAGE_TAG="$("$DIR"/scripts/git-version.sh)"

docker-compose build --parallel  --build-arg APP_VERSION="$IMAGE_TAG"

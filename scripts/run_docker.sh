#!/bin/bash
#set root directory
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )/.." >/dev/null 2>&1 && pwd )"
cd $DIR
# set common variables
set -a
[ -f .env ] && . .env
set +a
# set variables
: "${DOCKER_REGESTRY:="$DEFAULT_DOCKER_REGESTRY"}"
IMAGE_TAG="$($DIR/scripts/git-version.sh)"
TAG=$DOCKER_REGESTRY/$IMAGE_ID:$IMAGE_TAG

echo run docker image $TAG

docker run -it --rm -p 80:8080 $TAG $1

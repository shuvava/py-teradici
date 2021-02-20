#!/bin/bash

branch=$(git rev-parse --abbrev-ref HEAD)
latest=$(git tag  -l --merged master --sort='-*authordate' | head -n1)

semver_parts=(${latest//./ })
major=${semver_parts[0]:=0}
minor=${semver_parts[1]:=0}
patch=${semver_parts[2]:=0}

count=$(git rev-list HEAD ^${latest} --ancestry-path ${latest} --count)
version=""

case $branch in
   "master")
      version=${major}.$((minor+1)).0
      ;;
   "feature/*")
      version=${major}.${minor}.${patch}-${branch}-${count}
      ;;
   *)
      >&2 echo "unsupported branch type"
      exit 1
      ;;
esac

echo ${version}
exit 0

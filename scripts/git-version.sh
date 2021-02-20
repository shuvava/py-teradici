#!/bin/bash

branch=$(git rev-parse --abbrev-ref HEAD)
latest=$(git tag  -l --merged master --sort='-*authordate' | head -n1)

echo "${latest}"
semver_parts=(${latest//./ })
major=${semver_parts[0]//[vV]/}
if [ -z "$major" ]
then
    major="0"
fi

minor=${semver_parts[1]:=0}
patch=${semver_parts[2]:=0}

count=$(git rev-list HEAD ^${latest} --ancestry-path ${latest} --count)
if [ -z "$count" ]
then
    count="0"
fi
version="${major}.${minor}.${patch}.${count}"


echo ${version}
exit 0

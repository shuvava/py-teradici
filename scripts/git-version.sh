#!/bin/bash

branch=$(git rev-parse --abbrev-ref HEAD)
latest=$(git tag  -l --merged master --sort='-*authordate' | head -n1)

semver_parts=(${latest//./ })
major=${semver_parts[0]//[vV]/}
minor=${semver_parts[1]:=0}
patch=${semver_parts[2]:=0}

count=$(git rev-list HEAD ^${latest} --ancestry-path ${latest} --count)
version="${major}.${minor}.${patch}.${count}"


echo ${version}
exit 0

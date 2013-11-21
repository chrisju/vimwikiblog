#!/bin/bash

function check {
if [[ $? -ne 0 ]]; then
    exit
fi
}

git diff github master | git apply
check
git apply patch_open
check
rm patch_open

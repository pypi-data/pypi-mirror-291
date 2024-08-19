#!/bin/bash

# このファイルのあるディレクトリで実行
CULLENT_FILEDIR=$(
    cd "$(dirname "${0}")" || exit
    pwd
)
cd "$CULLENT_FILEDIR" || exit

git init

git config --global --add safe.directory /home/wanchiwanpu/mylib/workspace/tvtsplit

git add .

git commit -m "first commit"

git remote add origin git@github.com:anyumuenyumuboto/tvtsplit.git
git branch -M main
git push -u origin main


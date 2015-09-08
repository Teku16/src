@echo off
git fetch origin master --quiet
echo.Updated files!
cd ..
title Astron Server
astrond --loglevel info config/cluster.yml
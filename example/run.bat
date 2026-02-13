@echo off

pushd %~dp0%

py ../run.py -s tasks -l termrun.log

popd

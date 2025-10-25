@echo off

coverage erase

coverage run -m unittest discover -s tests

coverage report

pause
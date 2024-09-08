::@echo off
Python -m Chess
if %errorlevel% neq 0 (
	echo There was an error; exiting now.
) else (
	echo Compiled correctly!  Running Chess
)
pause
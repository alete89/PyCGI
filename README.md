[![Generic badge](https://img.shields.io/badge/Slack-open-<green>.svg)](https://mtrpc.slack.com/)


# PyCGI
A Configurable Graphic user Interface written in Python 2.7 and PyQt4

## Description
This app allows you to add any program or command into its menu and then launch them, capturing and showing its standard output in the main screen.

You can add a placeholder for parameters just by placing a hint between parentheses like this: `ping (enter some site)`. This will trigger a pop-up window before execution asking user to input a site to ping to ( [screenshot](#parameter) ). Note that the string between the parentheses is the hint given to the user in the pop-up.

A text editor is included within the app, it supports Python syntax highlighting for `.py` files.
App also includes a TreeView where you can browse local files in order to open them into the text editor.

Menus are loaded from a CSV (example is included), you can add, remove or edit them from the app itself (3rd tab)

## Usage
Windows: download latest zip release, which includes binaries and an example CSV with some menus pre-loaded.
Linux: download latest source from releases, launch by `python PyCGI.py` in main directory

## Screenshots:
![lanzando un script](https://user-images.githubusercontent.com/4999277/36319436-b029f710-1321-11e8-8099-fe7406b83f3f.png)
![editor de texto](https://user-images.githubusercontent.com/4999277/36319402-996a0e98-1321-11e8-8115-4e2e6fb4950e.png)
![editor de secuencias](https://user-images.githubusercontent.com/4999277/36319511-e2f57b38-1321-11e8-972b-d0b5d2fa370f.png)
### parameter
![pop-up parameter](https://user-images.githubusercontent.com/4999277/36320560-6441c478-1325-11e8-83f1-fd0e56badba2.png)



Tizen Package Generator
=======================

This project is meant to package a bunch of applications/games for Tizen Store
easily.

Works with Tizen SDK 2.1 and 2.2 beta.

Requeriments
------------

* A folder with all the games to be packaged
* A valid .p12 signature (generated by Tizen SDK) for signing your apps for Tizen Store
* A profiles.xml file (generated by Tizen SDK) for signing your apps for Tizen Store
* A json file with a basic configuration

JSON Configuration
------------------

You will need a json file where you should specify a basic configuration for
each application.

    {
        "TestGame1": {
            "name": "Test Game 1",
            "version": "1.0.0",
            "launch_path": "index.html",
            "app_identifier": "http://test.game1.com",
            "screen_orientation": "landscape"
        },
        "TestGame2": {
            "name": "Test Game 2",
            "version": "2.1.4",
            "launch_path": "index.html",
            "app_identifier": "http://test.game2.com",
            "screen_orientation": "portrait",
            "package": "EdhY6Tf57"
        }
    }

* TestGame1 is the folder name in your games folder
* package is an optional parameter to specify the Tizen package id if exists.

Usage
-----

Just open a terminal and type

    $ python tizen.py

This will start the process. First of all, the script will try to delete previous
output and temp folders (**out** and **tmp**).

By default, the script will look for applications in **input** folder, and will
read the configuration from **conf.json**, but of course, these parameters are
configurable:

    usage: tizen.py [-h] [-i] [-j JSON] [-I INPUT] [-p PROFILES] [-n PROFILE_NAME]
                [-k]

    optional arguments:
      -h, --help            show this help message and exit
      -i, --install         Install app after the packaging
      -j JSON, --json JSON  Configuration json file
      -I INPUT, --input INPUT
                            Input folder
      -p PROFILES, --profiles PROFILES
                            Profiles XML file
      -n PROFILE_NAME, --profile_name PROFILE_NAME
                            Signing profile name
      -k, --keep_temp       Do not delete temp files


Known Issues
-------------

Tizen SDK signing process fails:
https://developer.tizen.org/forums/sdk-ide/web-signing-cli-fails

Tizen Package Generator
=======================

This project is meant to package web applications for Tizen Store easily without
using the IDE (everything works through Tizen's SDK's CLI).

Works with Tizen SDK 2.1 and 2.2 beta.

Introduction to Tizen Pacakges
-------------------------------

A Tizen package consist of the following elements:

* A *.project* file
* A *config.xml* file
* The actual code of the application
* A valid png icon file (128x128)
* An *author-signature.xml* file (generated when signing the application)
* A *signature1.xml* file (generated when signing the application)

This script will generate a valid .wgt signed package

Requeriments
------------

* Tizen SDK installed (and $TIZEN_SKD_PATH defined in your path)
* A folder with the application(s) code
* A *profiles.xml* file (generated by Tizen SDK) for signing your apps for Tizen Store
* A valid *.p12* certificate (generated by Tizen SDK) for signing your apps for Tizen Store. This file will be referenced by your *profiles.xml* file.
* A json file with a basic configuration
* A 128x128 png icon file. This script will transform your icon to make it follow the
[Tizen Icons Guidelines](https://developer.tizen.org/documentation/ux-guide/visual-style/icons).
If your icon is already following them, it will suffer no changes.

Where to find Tizen SDK files:

**.p12 certificate** (referenced in *profiles.xml* file)

    TIZEN_SDK_FOLDER/tools/certificate-generator/your-certificate.p12

**profiles.xml**

    TIZEN_WORKSPACE_FOLDER/.metadata/.plugins/org.tizen.common.sign/profiles.xml

Dependencies
-------------

* [Python Imaging Library](https://pypi.python.org/pypi/PIL)

You can install it also with pip:

    $ pip install PIL

How to generate your profile
-----------------------------

Just in case you haven't already created your certificate and profile, and you
don't know how to do it, you just have to (once the SDK is installed) go to
Preferences > Tizen SDK > Security Profiles, and select "Add".

A new dialog will appear and you only have to fill the information. Once you
have created the profile, you will need to assign it an Author Certificate.

If you already have one, just select it, otherwise, the IDE will generate one
for you. Notice that you will need to use the same certificate for your
applications.

Now you can find those files in the specified paths.

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
            "screen_orientation": "landscape",
            "viewmodes": "fullscreen",
            "icon": "icon.png"
        },
        "TestGame2": {
            "name": "Test Game 2",
            "version": "2.1.4",
            "launch_path": "index.html",
            "app_identifier": "http://test.game2.com",
            "screen_orientation": "portrait",
            "viewmodes": "maximized",
            "icon": "icon.png",
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
output and temp folders (*out* and *tmp*).

By default, the script will look for applications in *input* folder, and will
read the configuration from *conf.json*, but of course, these parameters are
configurable:

    usage: tizen.py [-h] [-j JSON] [-I INPUT] [-i] [-k] [-s] [-p PROFILES]
                    [-n PROFILE_NAME]

    optional arguments:
      -h, --help            show this help message and exit
      -j JSON, --json JSON  Configuration json file (by default conf.json)
      -I INPUT, --input INPUT
                            Input folder (by default 'input')
      -i, --install         Install app after the packaging
      -k, --keep_temp       Do not delete temp files
      -s, --sign            Sign package
      -p PROFILES, --profiles PROFILES
                            Profiles XML file (required only if signing, if not
                            provided, Tizen SDK's default profile is used)
      -n PROFILE_NAME, --profile_name PROFILE_NAME
                            Signing profile name (required only if signing)

If you don't want to sing your application (for debugging for example), you
don't have to care about the profiles.xml file or the profile name.

If you are signing your application and you don't specify a profiles.xml file,
the default Tizen SDK's profiles.xml file will be used.

Official Documentation
-----------------------
[Tizen Documentation](https://developer.tizen.org/help/index.jsp?topic=%2Forg.tizen.web.appprogramming%2Fhtml%2Fide_sdk_tools%2Fcommand_line_interface.htm)


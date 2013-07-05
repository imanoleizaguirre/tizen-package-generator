# coding=utf-8

import json
import shutil
import os

from TizenPackage import TizenPackage

packages = []


def clean_up():
    """Removes the output and temp directories if they exist"""
    try:
        shutil.rmtree('out')
    except:
        pass

    try:
        shutil.rmtree('tmp')
    except:
        pass


def check_required_files():
    """Checks that all the required files are not missing"""
    try:
        os.environ['TIZEN_SDK_PATH']
    except (KeyError):
        raise IOError("Error: Cannot find the Tizen SDK. Please define "
                      "TIZEN_SDK_PATH as an env variable")

    if not os.path.isfile("games.json"):
        raise Exception("Missing games.json file")

    if not os.path.isfile("profiles.xml"):
        raise Exception("Missing profiles.xml file")

    if not os.listdir("games"):
        raise Exception("Input games folder is empty")


def generate_packages():
    """Generates the Tizen packages"""
    games_information = json.loads(open("games.json", 'r').read())

    for game, data in games_information.iteritems():
        try:
            tizen_package = TizenPackage("ludei", game, data)
            tizen_package.generate_package()
            packages.append(tizen_package)
        except:
            print "Error packaging %s" % game


def install_games():
    """Installs the generated packages"""
    for package in packages:
        package.install()


if __name__ == "__main__":
    clean_up()
    check_required_files()
    generate_packages()
    #install_games()

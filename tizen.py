# coding=utf-8

import json
import shutil
import os
import argparse

from TizenPackage import TizenPackage

packages = []
summary = {}


def remove_out_folder():
    try:
        shutil.rmtree('out')
    except:
        pass


def remove_tmp_folder():
    try:
        shutil.rmtree('tmp')
    except:
        pass


def clean_up():
    """Removes the output and temp directories if they exist"""
    remove_out_folder()
    remove_tmp_folder()


def check_required_files(input, json_file, profiles):
    """Checks that all the required files are not missing"""
    try:
        os.environ['TIZEN_SDK_PATH']
    except (KeyError):
        raise IOError("Error: Cannot find the Tizen SDK. Please define "
                      "TIZEN_SDK_PATH as an env variable")

    if not os.path.isfile(json_file):
        raise Exception("Missing configuration json file: %s" % json_file)

    if not os.path.isfile(profiles):
        raise Exception("Missing profiles.xml file")

    if not os.listdir(input):
        raise Exception("Input folder is empty")


def generate_packages(json_file, profile_name, profiles_file, input_folder):
    """Generates the Tizen packages"""
    input_information = json.loads(open(json_file, 'r').read())

    for input, data in input_information.iteritems():
        try:
            tizen_package = TizenPackage(profile_name, profiles_file,
                                         input_folder, input, data)
            wgt = tizen_package.generate_package()
            summary[input] = wgt
            if wgt:
                packages.append(tizen_package)

        except Exception, e:
            print "Error packaging %s: %s" % (input, e)


def install_apps():
    """Installs the generated packages"""
    for package in packages:
        package.install()
    else:
        print "No packages to install"


def print_summary():
    """Prints a summary of the packaging process"""
    print "\nSummary"
    print "=" * 8
    print
    for input, result in summary.iteritems():
        print "+ %s[%s]" % (input.ljust(30, "."), ['FAIL', 'OK'][result])


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--install",
                        help="Install app after the packaging",
                        action="store_true")
    parser.add_argument('-j', "--json", help="Configuration json file",
                        required=False, default="conf.json")
    parser.add_argument('-I', "--input", help="Input folder",
                        required=False, default="input")
    parser.add_argument('-p', "--profiles", help="Profiles XML file",
                        required=False, default="profiles.xml")
    parser.add_argument('-n', "--profile_name", help="Signing profile name",
                        required=False, default="test")
    parser.add_argument('-k', "--keep_temp", help="Do not delete temp files",
                        action="store_true")
    args = parser.parse_args()

    json_file = args.json
    profiles_file = args.profiles
    profile_name = args.profile_name
    input_folder = args.input

    clean_up()
    check_required_files(input_folder, json_file, profiles_file)
    generate_packages(json_file, profile_name, profiles_file, input_folder)
    print_summary()

    if not args.keep_temp:
        print "\nRemoving tmp folder."
        remove_tmp_folder()

    if args.install:
        print "\nInstalling apps"
        print "=" * 15
        print
        install_apps()

# coding=utf-8

import os
import string
import random
import shutil
import errno


class TizenPackage(object):
    """Generates a Tizen package"""

    def __init__(self, profile_name, game_folder_name, json):

        self.profile_name = profile_name
        self.source_folder = "games/%s" % game_folder_name
        self.tmp_folder = "tmp/%s" % game_folder_name
        self.game_folder_name = game_folder_name
        self.name = json['name']
        self.version = json['version']
        self.launchPath = json['launch_path']
        self.appIdentifier = json['app_identifier']
        self.screen_orientation = json['screen_orientation']
        try:
            self.package = json['package']
        except (KeyError):
            self.package = self._generate_tizen_app_id()

        try:
            self.icon = json['icon']
        except:
            self.icon = "icon.png"

    def __str__(self):
        return "Tizen package for %s (%s)" % (self.name, self.package)

    def _generate_tizen_app_id(self):
        """Generates a 10-character alphanumeric value used to identify
        a Tizen application"""
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for x in range(10))

    def _copy_game_files(self):
        """Copies the source file games"""
        try:
            shutil.copytree(self.source_folder, self.tmp_folder)
        except OSError as exc:
            if exc.errno == errno.ENOTDIR:
                shutil.copy(self.source_folder, self.tmp_folder)
            else:
                raise

    def _check_icon(self):
        """Checks that the folder contains a valid icon"""
        if not os.path.isfile("%s/%s" % (self.source_folder, self.icon)):
            raise Exception("Missing icon file. Please create a icon.png")

    def _generateXML(self):
        """Generates de configuration XML file"""

        print "...generating config.xml file."

        xml_template = open('templates/tizenConfigXML.txt', 'r').read()
        xml_content = xml_template.format(self.appIdentifier, self.version,
            self.package, self.name, self.launchPath, self.screen_orientation,
            self.icon)

        open("%s/config.xml" % self.tmp_folder, "w").write(xml_content)

    def _generateProjectFile(self):
        """Generates the configuration XML file"""

        print "...generating .project file."
        template = open('templates/tizenProjectTemplate.txt', 'r').read()
        content = template % (self.name)
        open("%s/.project" % self.tmp_folder, "w").write(content)

    def _generateTizenPackage(self):
        """Generates the Tizen package"""

        print "...packaging .wgt"

        os.system('$TIZEN_SDK_PATH/tools/ide/bin/./web-packaging out/%s.wgt %s'
            % (self.game_folder_name, self.tmp_folder))

    def _generate_signature(self):
        """Generates the signature profile for the future package"""
        print "...generating signature"

        os.system("$TIZEN_SDK_PATH/tools/ide/bin/./web-signing –p "
                  "%s:profiles.xml" % self.profile_name)

    def install(self):
        """Install a game on the device"""
        print "...installing game"
        os.system("$TIZEN_SDK_PATH/tools/ide/bin/./web-install -w %s.wgt"
            % self.game_folder_name)

    def generate_package(self):

        print "Generating Tizen package for %s" % self.name
        self._check_icon()
        self._copy_game_files()
        self._generateXML()
        self._generateProjectFile()
        self._generate_signature()
        self._generateTizenPackage()

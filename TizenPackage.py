# coding=utf-8

import os
import string
import random
import shutil
import errno

from PIL import Image, ImageOps


class TizenPackage(object):
    """Generates a Tizen package"""

    def __init__(self, profile_name, profiles_file, input_folder,
                 app_folder_name, json, sign):

        self.profiles_file = profiles_file
        self.input_folder = input_folder

        self.profile_name = profile_name
        self.source_folder = "%s/%s" % (input_folder, app_folder_name)
        self.tmp_folder = "tmp/%s" % app_folder_name
        self.app_folder_name = app_folder_name
        self.name = json['name']
        self.version = json['version']
        self.launchPath = json['launch_path']
        self.appIdentifier = json['app_identifier']
        self.screen_orientation = json['screen_orientation']
        self.viewmodes = json['viewmodes']
        self.icon = json['icon']
        self.sign = sign

        try:
            self.package = json['package']
        except (KeyError):
            self.package = self._generate_tizen_app_id()

    def __str__(self):
        return "Tizen package for %s (%s)" % (self.name, self.package)

    def _generate_tizen_app_id(self):
        """Generates a 10-character alphanumeric value used to identify
        a Tizen application"""

        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for x in range(10))

    def _copy_input_files(self):
        """Copies the source file input"""

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

    def _generate_config_xml(self):
        """Generates de configuration XML file"""

        print "...generating config.xml file."

        xml_template = open('templates/tizenConfigXML.txt', 'r').read()
        xml_content = xml_template.format(self.appIdentifier, self.version,
            self.package, self.name, self.launchPath, self.screen_orientation,
            self.icon, self.viewmodes)

        open("%s/config.xml" % self.tmp_folder, "w").write(xml_content)

    def _generate_dot_project_file(self):
        """Generates the configuration XML file"""

        print "...generating .project file."
        template = open('templates/tizenProjectTemplate.txt', 'r').read()
        content = template % (self.name)
        open("%s/.project" % self.tmp_folder, "w").write(content)

    def _generate_icon(self):
        """Generates a valid Tizen icon file (following UI Guidelines)"""

        print "... generating icon"

        mask = Image.open('mask.png').convert('L')
        im = Image.open("%s/%s" % (self.tmp_folder, self.icon))
        output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        output.save("%s/%s" % (self.tmp_folder, self.icon))

    def _generate_signature(self):
        """Generates the signature profile for the future package"""

        print "...generating signature"
        original_path = os.getcwd()
        os.chdir("tmp/%s" % self.app_folder_name)
        os.system("$TIZEN_SDK_PATH/tools/ide/bin/./web-signing -p "
            "%s%s" % (self.profile_name,
                (":" + str(self.profiles_file)) if self.profiles_file else ""))
        os.chdir(original_path)

    def _generateTizenPackage(self):
        """Generates the Tizen package"""

        print "...packaging .wgt"

        errors = os.system("$TIZEN_SDK_PATH/tools/ide/bin/./web-packaging "
                           "out/%s.wgt %s"
                           % (self.app_folder_name, self.tmp_folder))
        return not errors

    def install(self):
        """Install an app on the device"""
        print "...installing %s" % self.name
        os.system("$TIZEN_SDK_PATH/tools/ide/bin/./web-install -w out/%s.wgt"
                   % self.app_folder_name)

    def generate_package(self):

        print "\nGenerating Tizen package for %s" % self.name
        print "=" * (29 + len(self.name))

        try:
            self._check_icon()
        except Exception, e:
            print e
            return False

        self._copy_input_files()
        self._generate_config_xml()
        self._generate_icon()
        self._generate_dot_project_file()

        if self.sign:
            self._generate_signature()

        return self._generateTizenPackage()

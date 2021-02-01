import configparser
import os
import sys

class conf():

    #def __init__(self, name):
        #self.name = name

    def create(self, confFile):
        if os.path.exists(confFile):
            return 'File Exists, Doing Nothing'
        config = configparser.ConfigParser()
        with open(confFile, 'w') as configfile:
            config.write(configfile)

    def write(self, confFile, section, option, value):
        self.create(confFile)
        config = configparser.ConfigParser()
        config.read(confFile)
        print('read')
        if section in config.sections():
            config.set(section=section, option=option, value=value)
        else:
            print('no such section')
            config.add_section(section)
            config.set(section=section, option=option, value=value)
            config.write(sys.stdout)

    def read(self, confFile, section, arg, var):
        pass


conf = conf()


conf.write(confFile='config.ini', section='Pi25MCH', option='uri', value='http://192.168.122.25:8080')
conf.write(confFile='config.ini', section='Pi25MCH', option='uri2', value='http://192.168.122.25:8080')
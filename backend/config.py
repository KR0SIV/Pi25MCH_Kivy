import configparser
import os
import sys


class conf():
    #Getting config parser setup
    confFile = 'config.ini'
    config = configparser.ConfigParser()

    def __init__(self):#Let's check for a config file, if one doesn't exist we're going to populate a default config file.
        try:
            self.config.read('config.ini')
            op25uri = self.config.get('Pi25MCH', 'uri')

        except:#Failed to read a config file, let's populate a default config.
            self.config['Pi25MCH'] = {'uri': 'http://192.168.122.25:8080'}
            self.config['ScanMode'] = {'mode': 'list'}

            self.config['RadioReference'] = {'rruser': '',
                                        'rrpass':''}

            self.config['Menu Button Grid'] = {'callogging': 'False'}
            self.config['SDR'] = {'sdr': 'RTL',
                                 'lna': '45',
                                 'samplerate': '2.0e6'}

            with open(self.confFile, 'w') as configfile:
                self.config.write(configfile)

    def update(self, section, var, val):
        if self.config.has_section(section=section):
            self.config[section][var] = val
            with open(self.confFile, 'w') as configfile:
                self.config.write(configfile)
        else:
            raise ValueError('That section does not exist')
        if self.config.has_option(section=section, option=var):
            self.config[section][var] = val
            with open(self.confFile, 'w') as configfile:
                self.config.write(configfile)
        else:
            raise ValueError('That option does not exist!')



#conf = conf()

#conf.insert('Pi25MCH', 'uri', 'fuck')
#conf.update('Pi25MCH', 'uddffddfri', 'http://192.168.122.25:8080')
#conf.write(section='Pi25MCH', option='uri', value='http://192.168.122.25:8080')
#conf.write(confFile='config.ini', section='Pi25MCH', option='uri2', value='http://192.168.122.25:8080')
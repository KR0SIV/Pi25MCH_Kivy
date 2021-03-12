from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
#from kivymd.uix.tab import MDTabsBase
from kivy.properties import ObjectProperty
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.settings import Settings
from kivy.logger import Logger
from backend.config import op25config
from backend.config import rrconfig

import os

import re

# This JSON defines entries we want to appear in our App configuration screen



#from kivymd.material_resources import DEVICE_TYPE
from threading import Thread
from backend.updater import queryserver, jsoncmd


class Pi25mch(MDApp):
    previous_date = ObjectProperty()
    title = "Pi25: Mobile Control Head"

    data = {
        'pause-circle': 'Hold',
        'skip-next-circle': 'Skip',
        'lock': 'Lockout',
    }

    dialog = None


    def build(self):
        main_widget = Builder.load_file('kv/test.kv')
        self.bottom_navigation_remove_mobile(main_widget)
        Thread(target=lambda: queryserver(main_widget)).start()
        self.theme_cls.theme_style = "Light"  # "Light or Dark"
        #self.settings_cls = SettingsWithTabbedPanel
        return main_widget


    def build_config(self, config):
        """
        Set the default values for the configs sections.
        """
        config.setdefaults('OP25', {'URI': 'http://hostname:port'})
        config.setdefaults('Radio Reference', {'username': 'myUser', 'password': 'myPass' })


    def build_settings(self, settings):
        """
        Add our custom section to the default configuration object.
        """
        # We use the string defined above for our JSON, but it could also be
        # loaded from a file as follows:
        #     settings.add_json_panel('My Label', self.config, 'settings.json')
        settings.add_json_panel('OP25', self.config, data=op25config)
        settings.add_json_panel('Radio Reference', self.config, data=rrconfig)

    def on_config_change(self, config, section, key, value):
        """
        Respond to changes in the configuration.
        """
        Logger.info("main.py: App.on_config_change: {0}, {1}, {2}, {3}".format(
            config, section, key, value))

        if section == "OP25":
            if key == "URI":
                #self.root.ids.label.text = value
                pass


    def close_settings(self, settings=None):
        """
        The settings panel has been closed.
        """
        Logger.info("main.py: App.close_settings: {0}".format(settings))
        super(MDApp, self).close_settings(settings)


    class MySettings(Settings):
        """
        It is not usually necessary to create subclass of a settings panel. There
        are many built-in types that you can use out of the box
        (SettingsWithSidebar, SettingsWithSpinner etc.).
        You would only want to create a Settings subclass like this if you want to
        change the behavior or appearance of an existing Settings class.
        """

        def on_close(self):
            Logger.info("main.py: MySettings.on_close")

        def on_config_change(self, config, section, key, value):
            Logger.info(
                "main.py: MySettings.on_config_change: "
                "{0}, {1}, {2}, {3}".format(config, section, key, value))

    def bottom_navigation_remove_mobile(self, widget):
        # Removes some items from bottom-navigation demo when on mobile
        #if DEVICE_TYPE == 'mobile':
        #    widget.ids.bottom_navigation.remove_widget(widget.ids.bottom_navigation_desktop_2)
        #if DEVICE_TYPE == 'mobile' or DEVICE_TYPE == 'tablet':
        #    widget.ids.bottom_navigation.remove_widget(widget.ids.bottom_navigation_desktop_1)
        pass

    class ContentNavigationDrawer(BoxLayout):
        screen_manager = ObjectProperty()
        nav_drawer = ObjectProperty()



    class buttons():
        def hold(self, tg):
            Logger.info('Pressed Hold')
            id = str(re.findall('(?:.*)(?:ID:.)(\d{1,8})', tg)[0])
            if id == '0':
                pass#If there is no ID to hold, don't do anything
            else:
                if str(self.text) == 'HOLD':
                    jsoncmd('hold', int(id), '0')
                    #print(id)
                    self.text = str(id)
                else:
                    jsoncmd('hold', int(id), '0')
                    self.text = 'HOLD'

        def skip(self, tg):
            id = str(re.findall('(?:.*)(?:ID:.)(\d{1,8})', tg)[0])
            jsoncmd('skip', int(id), '0')
            Logger.info('Skipping TG: ' + str(tg))

        def lockout(self, tg):
            id = str(re.findall('(?:.*)(?:ID:.)(\d{1,8})', tg)[0])
            jsoncmd('lock', int(id), '0')
            Logger.info('Locking out TG: ' + str(tg))


#    class Tab(FloatLayout, MDTabsBase):
#        '''Class implementing content for a tab.'''
#        pass

    class ScrolllabelLabel(ScrollView):
        text = StringProperty('')

    class SettingsURI(BoxLayout):
        pass

    def show_confirmation_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Address:",
                type="custom",
                content_cls=self.SettingsURI,
                buttons=[
                    MDFlatButton(
                        text="CANCEL", text_color=self.theme_cls.primary_color
                    ),
                    MDFlatButton(
                        text="OK", text_color=self.theme_cls.primary_color
                    ),
                ],
            )
        self.dialog.open()

if __name__ == '__main__':
    Pi25mch().run()
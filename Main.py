from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.tab import MDTabsBase
from kivy.properties import ObjectProperty
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
import re



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
        main_widget = Builder.load_file('kv/main.kv')
        self.bottom_navigation_remove_mobile(main_widget)
        Thread(target=lambda: queryserver(main_widget)).start()
        self.theme_cls.theme_style = "Dark"  # "Light"
        return main_widget


    def bottom_navigation_remove_mobile(self, widget):
        # Removes some items from bottom-navigation demo when on mobile
        #if DEVICE_TYPE == 'mobile':
        #    widget.ids.bottom_navigation.remove_widget(widget.ids.bottom_navigation_desktop_2)
        #if DEVICE_TYPE == 'mobile' or DEVICE_TYPE == 'tablet':
        #    widget.ids.bottom_navigation.remove_widget(widget.ids.bottom_navigation_desktop_1)
        pass



    class buttons():
        def hold(self, tg):
            id = str(re.findall('(?:.*)(?:ID:.)(\d{1,8})', tg)[0])
            if id == '0':
                pass#If there is no ID to hold, don't do anything
            else:
                if str(self.text) == 'HOLD':
                    jsoncmd('hold', int(id), '0')
                    print(id)
                    self.text = str(id)
                else:
                    jsoncmd('hold', int(id), '0')
                    self.text = 'HOLD'

        def skip(self, tg):
            id = str(re.findall('(?:.*)(?:ID:.)(\d{1,8})', tg)[0])
            jsoncmd('skip', int(id), '0')

        def lockout(self, tg):
            id = str(re.findall('(?:.*)(?:ID:.)(\d{1,8})', tg)[0])
            jsoncmd('lock', int(id), '0')


    class Tab(FloatLayout, MDTabsBase):
        '''Class implementing content for a tab.'''
        pass

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
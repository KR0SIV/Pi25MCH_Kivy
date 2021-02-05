from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.tab import MDTabsBase
from kivy.properties import ObjectProperty
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty


#from kivymd.material_resources import DEVICE_TYPE
from threading import Thread
from backend.updater import queryserver

class Pi25mch(MDApp):
    previous_date = ObjectProperty()
    title = "Pi25: Mobile Control Head"

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

    class Tab(FloatLayout, MDTabsBase):
        '''Class implementing content for a tab.'''
        pass

    class ScrolllabelLabel(ScrollView):
        text = StringProperty('')

if __name__ == '__main__':
    Pi25mch().run()
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.material_resources import DEVICE_TYPE
from kivymd.theming import ThemeManager

#from backend import op25query
from threading import Thread

import requests
import json


def jsoncmd(command, arg1, arg2):
    uri = 'http://192.168.122.25'
    port = 8080
    return requests.post(uri + ':' + str(port), json=[{"command": command, "arg1": int(arg1), "arg2": int(arg2)}])


def queryserver():
    while True:
        try:
            r = jsoncmd("update", 0, 0)
            data = json.loads(r.content)
        except:
            data = []

        if data == []:
            pass
        else:
            # print(data)
            for i in data:
                try:
                    nac = str(hex(data[0]['nac']))
                    rawnac = str(data[0]['nac'])
                    wacn = str(hex(data[0]['wacn']))
                    tgid = str(data[0]['tgid'])
                    system = str(data[0]['system'])
                    sysid = str('Sys ID: ' + hex(data[0]['sysid']))
                    tag = str(data[0]['tag'])
                    offset = str(data[0]['fine_tune'])
                    freq = str(data[0]['freq'])
                except:
                    nac = ''
                    rawnac = ''
                    wacn = ''
                    tgid = ''
                    system = ''
                    sysid = ''
                    tag = ''
                    offset = ''
                    freq = ''
                try:
                    grpaddr = str(data[1]['grpaddr'])
                    enc = str(data[1]['encrypted'])
                    srcaddr = str(data[1]['srcaddr'])
                    rxchan = str(data[1][rawnac]['rxchan'])
                    txchan = str(data[1][rawnac]['txchan'])
                    rfid = str(data[1][rawnac]['rfid'])
                    stid = str(data[1][rawnac]['stid'])
                    secondary = str(data[1][rawnac]['secondary'])
                    adjacent_data = str(data[1][rawnac]['adjacent_data'])
                    frequencies = str(data[1][rawnac]['frequencies'])
                    tsbks = str(data[1][rawnac]['tsbks'])
                except:
                    grpaddr = ''
                    enc = ''
                    srcaddr = ''
                    rxchan = ''
                    txchan = ''
                    rfid = ''
                    stid = ''
                    secondary = ''
                    adjacent_data = ''
                    frequencies = ''
                    tsbks = ''

                result = {"nac": nac, "rawnac": rawnac, "wacn": wacn, "system": system, "sysid": sysid, "tag": tag,
                          "tgid": tgid, "offset": offset, "freq": freq,
                          "grpaddr": grpaddr, "enc": enc, "srcaddr": srcaddr, "rxchan": rxchan, "rfid": rfid,
                          "stid": stid, "secondary": secondary, "adjacent_data": adjacent_data,
                          "frequencies": frequencies,
                          "tsbks": tsbks, "txchan": txchan}
        try:
            return result
        except:
            pass


main_widget_kv = '''
#:import MDTextField kivymd.textfields.MDTextField
#:import MDBottomNavigation kivymd.tabs.MDBottomNavigation
#:import MDBottomNavigationItem kivymd.tabs.MDBottomNavigationItem


BoxLayout:
    orientation: 'vertical'
    ScreenManager:
        id: scr_mngr
        Screen:
            name: 'bottom_navigation'
            MDBottomNavigation:
                id: bottom_navigation_demo
                MDBottomNavigationItem:
                    name: 'octagon'
                    text: "SCANNER"
                    icon: "alert-octagon"
                    MDLabel:
                        id: scanner_label
                        font_style: 'Body1'
                        theme_text_color: 'Primary'
                        text: "SCANNER"
                        halign: 'center'
                MDBottomNavigationItem:
                    name: 'banking'
                    text: "LOGS"
                    icon: 'bank'
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_y: None
                        padding: dp(48)
                        spacing: 10
                        MDTextField:
                            hint_text: "You can put any widgets here"
                            helper_text: "Hello :)"
                            helper_text_mode: "on_focus"
                MDBottomNavigationItem:
                    name: 'bottom_navigation_desktop_1'
                    text: "SITE MODE"
                    icon: 'alert'
                    id: bottom_navigation_desktop_1
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_y: None
                        padding: dp(48)
                        spacing: 10
                        MDTextField:
                            hint_text: "Hello again"
                MDBottomNavigationItem:
                    name: 'bottom_navigation_desktop_2'
                    text: "SETTINGS"
                    icon: 'food'
                    id: bottom_navigation_desktop_2
                    MDLabel:
                        font_style: 'Body1'
                        theme_text_color: 'Primary'
                        text: "Cheese!"
                        halign: 'center'
        Screen:
            name: 'textfields'
            ScrollView:
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: self.minimum_height
                    padding: dp(48)
                    spacing: 10
                    MDTextField:
                        hint_text: "No helper text"
                    MDTextField:
                        hint_text: "Helper text on focus"
                        helper_text: "This will disappear when you click off"
                        helper_text_mode: "on_focus"
                    MDTextField:
                        hint_text: "Persistent helper text"
                        helper_text: "Text is always here"
                        helper_text_mode: "persistent"
                    MDTextField:
                        id: text_field_error
                        hint_text: "Helper text on error (Hit Enter with two characters here)"
                        helper_text: "Two is my least favorite number"
                        helper_text_mode: "on_error"
                    MDTextField:
                        hint_text: "Max text length = 10"
                        max_text_length: 10
                    MDTextField:
                        hint_text: "required = True"
                        required: True
                        helper_text_mode: "on_error"
                    MDTextField:
                        multiline: True
                        hint_text: "Multi-line text"
                        helper_text: "Messages are also supported here"
                        helper_text_mode: "persistent"
                    MDTextField:
                        hint_text: "color_mode = \'accent\'"
                        color_mode: 'accent'
                    MDTextField:
                        hint_text: "color_mode = \'custom\'"
                        color_mode: 'custom'
                        helper_text_mode: "on_focus"
                        helper_text: "Color is defined by \'line_color_focus\' property"
                        line_color_focus: self.theme_cls.opposite_bg_normal  # This is the color used by the textfield
                    MDTextField:
                        hint_text: "disabled = True"
                        disabled: True
'''




class Pi25mch(App):
    theme_cls = ThemeManager()
    previous_date = ObjectProperty()
    title = "Pi25: Mobile Control Head"

    def build(self):
        main_widget = Builder.load_string(main_widget_kv)
        # self.theme_cls.theme_style = 'Dark'


        main_widget.ids.scanner_label.text = str(return_value['tag'])


        main_widget.ids.text_field_error.bind(
            on_text_validate=self.set_error_message,
            on_focus=self.set_error_message)
        self.bottom_navigation_remove_mobile(main_widget)
        return main_widget

    def bottom_navigation_remove_mobile(self, widget):
        # Removes some items from bottom-navigation demo when on mobile
        if DEVICE_TYPE == 'mobile':
            widget.ids.bottom_navigation_demo.remove_widget(widget.ids.bottom_navigation_desktop_2)
        if DEVICE_TYPE == 'mobile' or DEVICE_TYPE == 'tablet':
            widget.ids.bottom_navigation_demo.remove_widget(widget.ids.bottom_navigation_desktop_1)


    def set_error_message(self, *args):
        if len(self.root.ids.text_field_error.text) == 2:
            self.root.ids.text_field_error.error = True
        else:
            self.root.ids.text_field_error.error = False



if __name__ == '__main__':
    import concurrent.futures

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(queryserver)
        return_value = future.result()
        #print(return_value)
    #Thread(target=queryserver).start()
    Pi25mch().run()




from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.material_resources import DEVICE_TYPE
from threading import Thread
import requests
import json


def jsoncmd(command, arg1, arg2):
    uri = 'http://192.168.122.25'
    port = 8080
    return requests.post(uri + ':' + str(port), json=[{"command": command, "arg1": int(arg1), "arg2": int(arg2)}])


def queryserver(widget):
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
                widget.ids.scanner_tag_label.text = str(result['tag'])


class Pi25mch(MDApp):
    #def __init__(**kwargs):
        #self.theme_cls.theme_style = "Dark"
   #     super().__init__(**kwargs)
    previous_date = ObjectProperty()
    title = "Pi25: Mobile Control Head"

    def build(self):
        #main_widget = Builder.load_string(main_widget_kv)
        main_widget = Builder.load_file('kv/main.kv')
        # self.theme_cls.theme_style = 'Dark'
#        main_widget.ids.scanner_label.text = str(return_value['tag'])
        self.bottom_navigation_remove_mobile(main_widget)

        Thread(target=lambda: queryserver(main_widget)).start()
        return main_widget

    def bottom_navigation_remove_mobile(self, widget):
        # Removes some items from bottom-navigation demo when on mobile
        if DEVICE_TYPE == 'mobile':
            widget.ids.bottom_navigation_demo.remove_widget(widget.ids.bottom_navigation_desktop_2)
        if DEVICE_TYPE == 'mobile' or DEVICE_TYPE == 'tablet':
            widget.ids.bottom_navigation_demo.remove_widget(widget.ids.bottom_navigation_desktop_1)




if __name__ == '__main__':
    Pi25mch().run()
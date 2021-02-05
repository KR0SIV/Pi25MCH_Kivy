import requests
import json
import time
from backend.logging import callLog



def jsoncmd(command, arg1, arg2):
    uri = 'http://192.168.122.25'
    port = 8080
    return requests.post(uri + ':' + str(port), json=[{"command": command, "arg1": int(arg1), "arg2": int(arg2)}])


def queryserver(widget):
    lastTag = ''
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
                    #It's not really a good idea to put alt text here as this exception is only thrown when something is missing.
                    #Tag text for example doesn't return null when nothing is there it returns an exmpty string so this exception doesn't run.
                    #Do not rely on these exceptions to change text, I mean I did it for grp and src addr but you still really shouldn't.
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
                    grpaddr = '0'
                    enc = ''
                    srcaddr = '0'
                    rxchan = ''
                    txchan = ''
                    rfid = ''
                    stid = ''
                    secondary = ''
                    adjacent_data = ''
                    frequencies = ''
                    tsbks = ''

                if tag == '':
                    tag = 'Scanning...'

                result = {"nac": nac, "rawnac": rawnac, "wacn": wacn, "system": system, "sysid": sysid, "tag": tag,
                          "tgid": tgid, "offset": offset, "freq": freq,
                          "grpaddr": grpaddr, "enc": enc, "srcaddr": srcaddr, "rxchan": rxchan, "rfid": rfid,
                          "stid": stid, "secondary": secondary, "adjacent_data": adjacent_data,
                          "frequencies": frequencies,"tsbks": tsbks, "txchan": txchan}

                ##Only update the display and call log if there is a valid ID for each field
                if grpaddr != '0' and srcaddr != '0':
                    widget.ids.scanner_tag_label.text = str(tag)
                    widget.ids.scanner_srcgrp_label.text = str('Radio ID: ' + srcaddr + '\r\n' + 'TalkGroup ID: ' + grpaddr)
                    widget.ids.scanner_system_label.text = str(system)

                    ##Call Logging
                    lastTag = callLog(lastTag, tag, result, widget)#Return the tag so you can assign it in your update loop
                else:
                    widget.ids.scanner_tag_label.text = 'Scanning...'
                    widget.ids.scanner_srcgrp_label.text = 'Radio ID: 0\r\nTalkGroup ID: 0'


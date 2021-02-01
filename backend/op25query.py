import requests
import json

uri = 'http://192.168.122.25'
port = 8080

#print(uri + ':' + str(port))

def jsoncmd(command, arg1, arg2):
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
            #print(data)
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

                result = {"nac":nac, "rawnac":rawnac,"wacn":wacn,"system":system,"sysid":sysid,"tag":tag,"tgid":tgid,"offset":offset,"freq":freq,
                          "grpaddr":grpaddr,"enc":enc,"srcaddr":srcaddr,"rxchan":rxchan,"rfid":rfid,"stid":stid,"secondary":secondary,"adjacent_data":adjacent_data,"frequencies":frequencies,
                          "tsbks":tsbks,"txchan":txchan}
        try:
            return result
        except:
            return {}



#queryserver()


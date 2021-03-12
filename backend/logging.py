import datetime
import re

##A mono-spaced font would do you wonders here!
##You're missing some RID and TGID when logging, check in on that!
def callLog(lastTag, tag, result, widget):
    if lastTag not in tag:
        if 'Scanning' not in tag:  # and result['grpaddr'] != '0'
            #'TAG'.ljust(16, ' ')[0:16] + 'TGID'.ljust(10, ' ')[0:10] + 'UID'.ljust(10, ' ')[0:10] + 'TIME'
            widget.ids.log_call_label.text = 'TAG'.ljust(16, ' ')[0:16] + 'TGID'.ljust(10, ' ')[0:10] + 'UID'.ljust(10, ' ')[0:10] + 'TIME\r\n'+\
                                             tag.ljust(16, '.')[0:16] + \
                                             result['grpaddr'].ljust(10, '.')[0:10] + \
                                             result['srcaddr'].ljust(10, '.')[0:10] + \
                                             str(str(datetime.datetime.now()) + '......') + '\r\n'\
                                             + re.sub('(TAG.*TIME\r\n)', '', widget.ids.log_call_label.text[0:1000])
    return tag
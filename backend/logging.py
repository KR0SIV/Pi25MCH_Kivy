import datetime

##A mono-spaced font would do you wonders here!
##You're missing some RID and TGID when logging, check in on that!
def callLog(lastTag, tag, result, widget):
    if lastTag not in tag:
        if 'Scanning' not in tag:  # and result['grpaddr'] != '0'
            widget.ids.log_call_label.text = widget.ids.log_call_label.text + \
                                             'Tag: ' + tag.ljust(16, ' ')[0:16] + \
                                             ' TGID: ' + result['grpaddr'].ljust(5, ' ')[0:5] + \
                                             ' RID: ' + result['srcaddr'].ljust(10, ' ')[0:10] + \
                                             ' Time: ' + str(' ' + str(datetime.datetime.now()) + ' ') + '\r\n'
    return tag
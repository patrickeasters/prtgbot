from slackbot.bot import respond_to
from slackbot.bot import listen_to
import prtg_helper
import re

@respond_to('^\s*pause ([\S]*)(?: for (.+))?', re.IGNORECASE)
def stats(message, device_name=None, reason=None):
    if device_name == 'None':
        message.reply('Specify a device name, fool!')
    else:
        did = prtg_helper.get_deviceid(device_name)
        if not did:
            message.reply('Failed to find device: '+device_name)
        else:
            if reason:
                pause_reason = reason+' via prtgbot on slack'
            else:
                pause_reason = 'paused via prtgbot on slack'
            
            if prtg_helper.pause_device(did, 1, reason=pause_reason):
                message.reply(device_name+' has been paused')
            else:
                message.reply('Failed to pause device!')


@respond_to('^\s*unpause (.*)', re.IGNORECASE)
@respond_to('^\s*resume (.*)', re.IGNORECASE)
def stats(message, device_name=None):
    if device_name == 'None':
        message.reply('Specify a device name, fool!')
    else:
        did = prtg_helper.get_deviceid(device_name)
        if not did:
            message.reply('Failed to find device: '+device_name)
        else:
            if prtg_helper.pause_device(did, 0):
                message.reply(device_name+' has been unpaused')
            else:
                message.reply('Failed to unpause device!')


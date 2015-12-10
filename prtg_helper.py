from urllib2 import Request, urlopen, URLError
from urllib import urlencode
import json
import xml.etree.ElementTree as ET
import slackbot_settings

def api_call(path, params):
    
    # determine URL for PRTG API
    if (slackbot_settings.PRTG_URL).endswith('/'):
        url = (slackbot_settings.PRTG_URL).rstrip('/') + path
    else:
        url = slackbot_settings.PRTG_URL + path

    # build parameters
    params['username'] = slackbot_settings.PRTG_API_USER
    params['passhash'] = slackbot_settings.PRTG_API_PASSHASH

    data = urlencode(params)

    url = url + '?' + data
    req = Request(url)
    try:
        response = urlopen(req)
    except URLError as e:
        pass
    else:
        return response

    return 0



def pause_device(device_id, paused, reason="paused by prtgbot"):
    # set paused var for api_call
    if paused:
        pause_action = 0
    else:
        pause_action = 1

    # make the API call
    resp = api_call('/api/pause.htm', {'id':device_id, 'pausemsg':reason, 'action':pause_action})            
    if(resp):
        return True
    resp.close()

    return False

def get_deviceid(device_name):
    # do an API call and get results
    check_resp = api_call('/api/table.json', {'content':'devices', 'output':'json', 'columns':'objid,device,host,group,active'})
    
    if not check_resp:
        raise Exception('Bad URL response')
        return 0

    check_result = json.loads( check_resp.read() )

    check_resp.close()

    device_id = 0

    # iterate through list of devices and see if we can find a match by device name or host
    for dev in check_result['devices']:
        # check by name
        if device_name.lower() in dev['device'].lower():
            device_id = dev['objid']
            break

        # check by host
        if device_name.lower() == dev['host'].lower():
            device_id = dev['objid']
            break

    return device_id
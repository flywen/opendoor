# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from .WXBizMsgCrypt import WXBizMsgCrypt
import relay
import xml.etree.cElementTree as ET
import RPi.GPIO as GPIO
import time
import threading
import re

def wxent(req):
    msg_signature = req.GET.get('msg_signature', False)
    timestamp = req.GET.get('timestamp', False)
    nonce = req.GET.get('nonce', False)
    wxcpt = WXBizMsgCrypt('1fAR', '1JIZBlAuGpnzi1AVToUrwrtX7Mgc4UBCxfT8I3fD8vC', 'wwb1d49be5532d2965')
    if req.method == 'GET':
        echostr = req.GET.get('echostr', False)
        ret, sEchoStr = wxcpt.VerifyURL(msg_signature, timestamp, nonce, echostr)
        if (ret != 0):
            ret_val = "ERR: VerifyURL ret: " + str(ret)
            return ret_val
        return HttpResponse(sEchoStr)
    elif req.method == 'POST':
#        print 1
        data = req.body  # not POST
        ret, sMsg = wxcpt.DecryptMsg(data, msg_signature, timestamp, nonce)
#        if (ret != 0):
#           ret_val = "ERR: DecryptMsg ret: " + str(ret)
#           return HttpResponse(ret_val)

        xml_tree = ET.fromstring(sMsg)
        from_uid = xml_tree.find('FromUserName').text
        #content = xml_tree.find('Content').text
        msg_tpye = xml_tree.find('MsgType').text
        event = xml_tree.find('Event').text
        if event == 'scancode_push':
            scanresult = xml_tree.find('ScanCodeInfo').find('ScanResult').text
            #print "your id is:%s" % from_uid
            #print msg_tpye
            #print event
            #print scanresult
            door_no = re.search(r'opendoor/(.*)',scanresult).group(1)
            t_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            print "%s|INFO|USER:%s|DOOR_NO:%s" % (t_now, from_uid, door_no)
            if door_no == '1':
                no = 29
            elif door_no == '2':
                no = 31
            elif door_no == '3':
                no = 33
            elif door_no == '4':
                no = 35
            elif door_no == '5':
                no = 37
            elif door_no == '6':
                no = 32
            elif door_no == '7':
                no = 36
            elif door_no == '8':
                no = 38
            elif door_no == '9':
                no = 40
            #print no
            #print "%s|INFO|USER:%s|DOOR_NO:%s" % (t_now, from_uid, door_no)
            relay_open = threading.Thread(target=relay.relay,args=(no,)) 
            relay_open.start()
        #print content

        #sRespData = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[wx1009c4a861b4b621]]></FromUserName><CreateTime>1348831860</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><MsgId>1</MsgId><AgentID>1000002</AgentID></xml>" % (from_uid, 'you saied:dfas' + content,)
        #ret, sEncryptMsg = wxcpt.EncryptMsg(sRespData, nonce, timestamp)
        #return HttpResponse(sEncryptMsg)

    return HttpResponse("http method not suppoted")


def door01(req):
    print "This is door01, it is a demo."
    return render_to_response("1.html")

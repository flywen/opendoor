# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from .WXBizMsgCrypt import WXBizMsgCrypt
import xml.etree.cElementTree as ET

def wxent(req):
    msg_signature = req.GET.get('msg_signature', False)
    timestamp = req.GET.get('timestamp', False)
    nonce = req.GET.get('nonce', False)
    wxcpt = WXBizMsgCrypt('1fAR', '1JIZBlAuGpnzi1AVToUrwrtX7Mgc4UBCxfT8I3fD8vC', 'wx1009c4a861b4b621')
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
            print "用户:%s" % from_uid
            print msg_tpye
            print event
            print scanresult
        #print content

        #sRespData = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[wx1009c4a861b4b621]]></FromUserName><CreateTime>1348831860</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><MsgId>1</MsgId><AgentID>1000002</AgentID></xml>" % (from_uid, 'you saied:dfas' + content,)
        #ret, sEncryptMsg = wxcpt.EncryptMsg(sRespData, nonce, timestamp)
        #return HttpResponse(sEncryptMsg)

    return HttpResponse("http method not suppoted")


def door01(req):
    return render_to_response("1.html")

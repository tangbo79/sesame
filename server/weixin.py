# coding=utf-8
import hashlib
import msg_parser
import controller

from server import app
from flask import request, make_response

import logging

_logger = logging.getLogger(__name__)

@app.route('/', methods=['GET', 'POST'])
def weixin():
    if request.method == 'GET':
        if len(request.args) > 3:
            temparr = []
            token = "weixin"
            signature = request.args["signature"]
            timestamp = request.args["timestamp"]
            nonce = request.args["nonce"]
            echostr = request.args["echostr"]
            temparr.append(token)
            temparr.append(timestamp)
            temparr.append(nonce)
            temparr.sort()
            newstr = "".join(temparr)
            sha1str = hashlib.sha1(newstr)
            temp = sha1str.hexdigest()
            print "-----------------------------------"
            print "signature", signature, "temp", temp
            print "-----------------------------------"
            if signature == temp:
                return echostr
            else:
                return "认证失败，不是微信服务器的请求！"
        else:
            return "你请求的方法是：" + request.method
    else:  # POST
        print "POST"
        xmldict = msg_parser.recv_msg(request.data)
        _logger.info("process %s stock" % xmldict['Content']) 
        controller.process(xmldict)
        _logger.info("-----------------------------------")
        _logger.info("process result : %s" % xmldict['Content']) 
        _logger.info("-----------------------------------")
        reply = msg_parser.submit_msg(xmldict)
        response = make_response(reply)
        response.content_type = 'application/xml'
        print response
        return response


if __name__ == '__main__':
    print "hello"
    app.run(host='0.0.0.0', port=80, debug=True)


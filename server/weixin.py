# coding=utf-8
import hashlib
import msg_parser
import controller

from server import app
from flask import request, make_response

import logging

_logger = logging.getLogger(__name__)

def authenticate(request):
    if len(request.args) <= 3:
        return False
    token = "weixin"
    signature = request.args["signature"]
    timestamp = request.args["timestamp"]
    nonce = request.args["nonce"]
    echostr = request.args["echostr"]

    combine = "".join([signature, timestamp, nonce, echostr].sort())
    calcualte_signature = hashlib.sha1(combine).hexdigest()
    if calculate_signature == signature:
        return True
    else:
        return False

def process_user_request(request):
    xmldict = msg_parser.recv_msg(request.data)
    _logger.info("request = %r" % xmldict)
    _logger.info("process %s stock" % xmldict['Content']) 
    controller.process(xmldict)
    _logger.info("process result : %s" % xmldict['Content']) 
    reply = msg_parser.submit_msg(xmldict)
    response = make_response(reply)
    response.content_type = 'application/xml'
    _logger.info("response = %r" % response)
    return response

@app.route('/', methods=['GET', 'POST'])
def weixin():
    _logger.info("request method = %r" % request.method)
    if request.method == 'GET':
        try:
            if authenticate(request) == True:
                return echostr
            else:
                return "认证失败，不是微信服务器的请求！"
        except Exception as e:
            _logger.exception(e)
            return "you request is illegal"
    else:  # POST
        try:
            response = process_user_request(request)
        except Exception as e:
            _logger.exception(e)
            response = "you request is invalid"
        _logger.info("POST finished.")
        return response

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=80, debug=True)
    except Exception as e:
        _logger.exception(e)


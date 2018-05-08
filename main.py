#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response
import textRank
import test

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    print("starting processRequest...", req.get("result").get("action"))
    if req.get("result").get("action") != "newsnews":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    zone = parameters.get("news_category")

    cost = {'정치':textRank.politic + '\n' + test.politic_link,'경제':textRank.economy + '\n' + test.economy_link,
            '사회':textRank.social + '\n' + test.social_link, '문화':textRank.culture + '\n' + test.culture_link,
            '세계':textRank.world + '\n' + test.world_link, '아이티':textRank.IT + '\n' + test.IT_link}

    speech = cost[zone]
    print("Response:")
    print(speech)
    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        #"contextOut": [],
        "source": "Newscategory"
    }

@app.route('/static_reply', methods=['POST'])
def static_reply():
    speech = "Hello there, this reply is from the webhook !! "
    my_result =  {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }
    res = json.dumps(my_result, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

if __name__ == '__main__':
    port = int(os.getenv('PORT', 80))

    print ("Starting app on port %d" %(port))

    app.run(debug=True, port=port, host='0.0.0.0')
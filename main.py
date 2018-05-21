#!/usr/bin/env python
import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response
import crolling
import textRank
import crolling_issue
from random import *
from firebase import firebase


# Flask app should start in global layout
app = Flask(__name__)

# firebase database for android push
push_link = [crolling.politic_link1, crolling.economy_link1, crolling.social_link1, crolling.culture_link1, crolling.world_link1, crolling.IT_link1]
push_title = [crolling.politic_title1, crolling.economy_title1, crolling.social_title1, crolling.culture_title1, crolling.world_title1, crolling.IT_title1]
push_summary = [textRank.politic1, textRank.economy1, textRank.social1, textRank.culture1, textRank.world1, textRank.IT1]
push_num = randint(0,5)
firebase = firebase.FirebaseApplication('https://newssenger-69a99.firebaseio.com/')
while 1:
    if push_summary[push_num]=='': # summary가
        push_num = randint(0,5)
    else : break
firebase.post('/all/notification', {'name':'pushNotification','title':push_title[push_num],'text': push_summary[push_num]})
firebase.post('/all/chat', {'name':'pushNotification','text': push_link[push_num] + '@요약문장 ▶ ' + push_summary[push_num]})


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
    if req.get("result").get("action") == "newsnews":
        result = req.get("result")
        parameters = result.get("parameters")
        zone = parameters.get("news_category")
        num = randint(1,5)

        cost = {'정치':{1: crolling.politic_link1 + '@요약문장 ▶ ' + textRank.politic1,
                      2: crolling.politic_link2 + '@요약문장 ▶ ' + textRank.politic2,
                      3: crolling.politic_link3 + '@요약문장 ▶ ' + textRank.politic3,
                      4: crolling.politic_link4 + '@요약문장 ▶ ' + textRank.politic4,
                      5: crolling.politic_link5 + '@요약문장 ▶ ' + textRank.politic5},
                '경제':{1: crolling.economy_link1 + '@요약문장 ▶ ' + textRank.economy1,
                      2: crolling.economy_link2 + '@요약문장 ▶ ' + textRank.economy2,
                      3: crolling.economy_link3 + '@요약문장 ▶ ' + textRank.economy3,
                      4: crolling.economy_link4 + '@요약문장 ▶ ' + textRank.economy4,
                      5: crolling.economy_link5 + '@요약문장 ▶ ' + textRank.economy5},
                '문화': {1: crolling.culture_link1 + '@요약문장 ▶ ' + textRank.culture1,
                       2: crolling.culture_link2 + '@요약문장 ▶ ' + textRank.culture2,
                       3: crolling.culture_link3 + '@요약문장 ▶ ' + textRank.culture3,
                       4: crolling.culture_link4 + '@요약문장 ▶ ' + textRank.culture4,
                       5: crolling.culture_link5 + '@요약문장 ▶ ' + textRank.culture5},
                '세계':{1: crolling.world_link1 + '@요약문장 ▶ ' + textRank.world1,
                      2: crolling.world_link2 + '@요약문장 ▶ ' + textRank.world2,
                      3: crolling.world_link3 + '@요약문장 ▶ ' + textRank.world3,
                      4: crolling.world_link4 + '@요약문장 ▶ ' + textRank.world4,
                      5: crolling.world_link5 + '@요약문장 ▶ ' + textRank.world5},
                '사회': {1: crolling.social_link1 + '@요약문장 ▶ ' + textRank.social1,
                       2: crolling.social_link2 + '@요약문장 ▶ ' + textRank.social2,
                       3: crolling.social_link3 + '@요약문장 ▶ ' + textRank.social3,
                       4: crolling.social_link4 + '@요약문장 ▶ ' + textRank.social4,
                       5: crolling.social_link5 + '@요약문장 ▶ ' + textRank.social5},
                '아이티': {1: crolling.IT_link1 + '@요약문장 ▶ ' + textRank.IT1,
                       2: crolling.IT_link2 + '@요약문장 ▶ ' + textRank.IT2,
                       3: crolling.IT_link3 + '@요약문장 ▶ ' + textRank.IT3,
                       4: crolling.IT_link4 + '@요약문장 ▶ ' + textRank.IT4,
                       5: crolling.IT_link5 + '@요약문장 ▶ ' + textRank.IT5}}

        speech = cost[zone][num]
        if speech[-1] == '▶' : speech = "죄송해요. 다시 한 번 말씀해주세요. 😢@null"
    elif req.get("result").get("action") == "issueissue":
        speech = "오늘의 실시간 이슈는 " + ', '.join(crolling_issue.issue) + "입니다. 😊💓@null"
    else: return{}

    print("Response:")
    print(speech)
    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        #"contextOut": [],
        "source": "Newssenger"
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
    app.run(debug=False, port=port, host='0.0.0.0')


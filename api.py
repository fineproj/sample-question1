import flask
from flask import request,jsonify
import requests
import json
from datetime import datetime

app = flask.Flask(__name__)
app.config["DEBUG"] = True
time_format = "%Y-%m-%dT%H:%M:%SZ"

url = 'https://gitlab.com/-/snippets/2094509/raw/master/sample_json_1.json'
r = requests.get(url)
data = r.content
system_data = json.loads(data)

@app.route('/', methods=['GET'])
def home():
    return "<h1>Home</h1>"

@app.route('/api/produnit/all', methods=['GET'])
def api_all():
    return jsonify(system_data)

@app.route('/api/produnit', methods=['GET'])
def api_time():
    if 'start_time'in request.args:
        start_time = datetime.strptime(str(request.args['start_time']),time_format)
        print(start_time)
    
    if 'end_time'in request.args:
        end_time = datetime.strptime(str(request.args['end_time']),time_format)
        print(end_time)

    result_dict = {
        "shiftA" :{ "production_A_count" :0, "production_B_count" :0},
        "shiftB" :{ "production_A_count" :0, "production_B_count" :0},
        "shiftC" :{ "production_A_count" :0, "production_B_count" :0},
        }

    sixAm = datetime.strptime('06:00:00', "%H:%M:%S").time()
    twoPM = datetime.strptime('14:00:00', "%H:%M:%S").time()
    eightPM = datetime.strptime('20:00:00', "%H:%M:%S").time()
    elevenFiftyNine = datetime.strptime('23:59:59', "%H:%M:%S").time()
    twelveAM = datetime.strptime('00:00:00', "%H:%M:%S").time()

    for data in system_data:
        current_time = datetime.strptime(str(data['time']),"%Y-%m-%d %H:%M:%S")
        if  (start_time <= current_time <= end_time) and ( sixAm <= current_time.time() <= twoPM ) and data['production_A']==True:
            result_dict['shiftA']['production_A_count'] = result_dict['shiftA']['production_A_count'] + 1
      
        if  (start_time <= current_time <= end_time) and ( sixAm <= current_time.time() <= twoPM ) and data['production_B']==True:
            result_dict['shiftA']['production_B_count'] = result_dict['shiftA']['production_B_count'] + 1
      
        if  (start_time <= current_time <= end_time) and ( twoPM <= current_time.time() <= eightPM ) and data['production_A']==True:
            result_dict['shiftB']['production_A_count'] = result_dict['shiftB']['production_A_count'] + 1
        
        if  (start_time <= current_time <= end_time) and ( twoPM <= current_time.time() <= eightPM ) and data['production_B']==True:
            result_dict['shiftB']['production_B_count'] = result_dict['shiftB']['production_B_count'] + 1

        if  (start_time <= current_time <= end_time) and (( eightPM <= current_time.time() <= elevenFiftyNine ) or ( twelveAM <= current_time.time() <= sixAm )) and data['production_A']==True:
            result_dict['shiftC']['production_A_count'] = result_dict['shiftC']['production_A_count'] + 1
        
        if  (start_time <= current_time <= end_time) and (( eightPM <= current_time.time() <= elevenFiftyNine ) or ( twelveAM <= current_time.time() <= sixAm )) and data['production_B']==True:
            result_dict['shiftC']['production_B_count'] = result_dict['shiftC']['production_B_count'] + 1

    return jsonify(result_dict)
app.run()


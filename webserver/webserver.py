from flask import Flask, json
import requests
import sys

HOST = sys.argv[1]
PORT = sys.argv[2]

app = Flask(__name__)

def home_page(r):

    text = json.loads(r.content)
    strTable = """<html><table border="1"><tr><th>Sensor</th><th>Datetime</th><th>Status</th><th>Decision Time</th></tr>"""
    if text:
        print(text)
        for sensor in text:
            strTable += "<tr><td>{}</td>".format(sensor)
            strTable += "<td>{}</td>".format(text[sensor]['datetime'])
            strTable += "<td>{}</td>".format(text[sensor]['status'])
            strTable += "<td>{}</td>".format(text[sensor]['time_of_decision'])
            strTable += "</tr>"
        strTable += "</table></html>"
    else:
        strTable += "<tr><td>{}</td>".format('No sensors!!!')
        strTable += "</tr>"   
    return strTable

@app.route('/')
def status():

    try:
        r = requests.get("https://{0}:5000/sensors".format(sys.argv[3]), verify=False)
        if r.status_code != 200:
            print (r.status_code)
        response = home_page(r)
        return response

    except Exception as e:
        return 'Something wrong'

if __name__ == '__main__':
    app.run(host=HOST,port=PORT)
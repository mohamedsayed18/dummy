from flask import Flask, json
import requests

app = Flask(__name__)

def home_page(r):
    text = json.loads(r.content)
    strTable = """<html><table border="1"><tr><th>Sensor</th><th>Datetime</th><th>Status</th><th>Decision Time</th></tr>"""

    for sensor in text:
        strTable += "<tr><td>{}</td>".format(sensor)
        strTable += "<td>{}</td>".format(text[sensor]['datetime'])
        strTable += "<td>{}</td>".format(text[sensor]['status'])
        strTable += "<td>{}</td>".format(text[sensor]['time_of_decision'])
        strTable += "</tr>"
    strTable += "</table></html>"

    return strTable

@app.route('/')
def status():

    try:
        r = requests.get("https://127.0.0.1:5000/sensors", verify=False)
        if r.status_code != 200:
            print (r.status_code)
        response = home_page(r)
        return response

    except Exception as e:
        return 'Something wrong'

if __name__ == '__main__':
    app.run(port=8000)
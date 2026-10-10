
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, send
from scapy.all import *
from scapy.layers.http import HTTPRequest
app = Flask(__name__)  
sio = SocketIO(app, async_mode='threading')  
bl = set()
logs = []
def block(ip):
    if ip not in bl:
        bl.add(ip)
        cmd = (
              f'iptables -A INPUT -s {ip} -j DROP',
              f'iptables -A OUTPUT -d {ip} -j DROP'
             )
        [os.system(c) for c in cmd]
def handle(a):
    if not (a.haslayer(HTTPRequest) and a.haslayer(IP)):
        return
    http, src = a[HTTPRequest], a[IP].src
    uri = f"{http.Host.decode('utf-8', 'ignore')}{http.Path.decode('utf-8', 'ignore')}"
    if 'Cookie' in http.fields:
        cookie = http.Cookie.decode('utf-8', 'ignore')
        if cookie.strip().endswith(';'):
            logs.append({'type': 'cookie', 'ip': src, 'uri': uri, 'cookie': cookie})
         
            block(src)
            sio.send(logs[-1])
            return
    if "/shell.jsp" in uri or "/shell.aspx" in uri:
        logs.append({'type': 'url', 'ip': src, 'uri': uri})
        block(src)
        sio.send(logs[-1])
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/start_monitoring', methods=['POST'])
def start():
    sio.start_background_task(sniff, prn=handle, store=0, iface='ens33')
    return jsonify({'status': 'started'})
if __name__ == '__main__':
    sio.run(app, host='0.0.0.0', port=5100, allow_unsafe_werkzeug=True)

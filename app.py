from flask import Flask, render_template, request, send_file, jsonify
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

def generate_script(locations, action, script_type):
    script = ""
    for loc, ip_a, ip_b, ip_c, ip_d, lport_udp_b, lport_udp_c in locations:
        if script_type == "enum": 
            if action == "config":
                script += f"ENT-CARD:LOC={loc}:TYPE=SLIC:APPL=ENUMHC\n"
                script += f"CHG-IP-LNK:PORT=A:SUBMASK=255.255.255.0:MCAST=YES:IPADDR={ip_a}:LOC={loc}:DUPLEX=FULL:SPEED=1000\n"
                script += f"CHG-IP-LNK:PORT=B:SUBMASK=255.255.255.0:MCAST=NO:auto=no:IPADDR={ip_b}:LOC={loc}:DUPLEX=FULL:SPEED=100\n"
                script += f"CHG-IP-LNK:PORT=C:SUBMASK=255.255.255.0:MCAST=NO:auto=no:IPADDR={ip_c}:LOC={loc}:DUPLEX=FULL:SPEED=100\n"
                script += f"CHG-IP-LNK:PORT=D:SUBMASK=255.255.255.0:MCAST=YES:IPADDR={ip_d}:LOC={loc}:DUPLEX=FULL:SPEED=1000\n"
                script += f"CHG-IP-CARD:LOC={loc}:DOMAIN=TEKELEC.COM:DEFROUTER={'.'.join(ip_b.split('.')[:3]) + '.1'}\n"
                script += f"ENT-IP-HOST:HOST=enum.{loc}b:IPADDR={ip_b}:TYPE=LOCAL\n"
                script += f"ENT-IP-HOST:HOST=enum.{loc}c:IPADDR={ip_c}:TYPE=LOCAL\n"
                script += f"ENT-IP-CONN:LPORT={lport_udp_b}:LHOST=enum.{loc}b:PROT=UDP:CNAME=c{loc}b\n"
                script += f"ENT-IP-CONN:LPORT={lport_udp_c}:LHOST=enum.{loc}c:PROT=UDP:CNAME=C{loc}c\n"
                script += f"CHG-IP-CONN:CNAME=C{loc}:OPEN=YES\n"
                script += f"CHG-IP-CONN:CNAME=C{loc}a:OPEN=YES\n"
                script += f"Alw-card:loc={loc}\n\n"

            elif action == "delete":
                script += f"inh-card:loc={loc}\n"
                script += f"CHG-IP-CONN:CNAME=C{loc}:OPEN=No\n"
                script += f"CHG-IP-CONN:CNAME=C{loc}a:OPEN=No\n"
                script += f"DLT-IP-CONN:CNAME=c{loc}b\n"
                script += f"DLT-IP-CONN:CNAME=C{loc}c\n"
                script += f"DLT-IP-HOST:HOST=enum.{loc}b\n"
                script += f"DLT-IP-HOST:HOST=enum.{loc}c\n"
                script += f"CHG-IP-CARD:LOC={loc}:DEFROUTER=0.0.0.0\n"
                script += f"CHG-IP-LNK:PORT=A:IPADDR=0.0.0.0:LOC={loc}:\n"
                script += f"CHG-IP-LNK:PORT=B:IPADDR=0.0.0.0:LOC={loc}:\n"
                script += f"CHG-IP-LNK:PORT=C:IPADDR=0.0.0.0:LOC={loc}:\n"
                script += f"CHG-IP-LNK:PORT=D:IPADDR=0.0.0.0:LOC={loc}:\n"
                script += f"DLT-CARD:LOC={loc}\n\n"

        elif script_type == "sccp": 
            if action == "config":
                script += f"ENT-CARD:loc={loc}:TYPE=SLIC:APPL=vsccp\n"
                script += f"CHG-IP-LNK:PORT=A:SUBMASK=255.255.255.0:MCAST=YES:IPADDR={ip_a}:LOC={loc}:DUPLEX=FULL:SPEED=1000\n"
                script += f"CHG-IP-LNK:PORT=B:SUBMASK=255.255.255.0:MCAST=YES:IPADDR={ip_b}:LOC={loc}:DUPLEX=FULL:SPEED=1000\n"
                script += f"CHG-IP-CARD:LOC={loc}:DOMAIN=TEKELEC.COM:DEFROUTER=192.168.120.250\n"
                script += f"Alw-card:loc={loc}\n\n"

            elif action == "delete":
                script += f"inh-card:loc={loc}\n"
                script += f"CHG-IP-CARD:LOC={loc}:DEFROUTER=0.0.0.0\n"
                script += f"CHG-IP-LNK:PORT=A:IPADDR=0.0.0.0:LOC={loc}:\n"
                script += f"CHG-IP-LNK:PORT=B:IPADDR=0.0.0.0:LOC={loc}:\n"
                script += f"DLT-CARD:LOC={loc}\n\n"

        elif script_type == "ipsm": 
            if action == "config":
                script += f"ENT-CARD:loc={loc}:TYPE=IPSM:APPL=ips\n"
                script += f"CHG-IP-LNK:PORT=A:SUBMASK=255.255.255.0:MCAST=YES:IPADDR={ip_a}:LOC={loc}:DUPLEX=FULL:SPEED=100\n"
                script += f"ENT-IP-HOST:HOST=ipsm{loc}:ipaddr={ip_a}\n"
                script += f"CHG-IP-CARD:LOC={loc}:DOMAIN=new{loc}.com:DEFROUTER={'.'.join(ip_a.split('.')[:3]) + '.1'}\n"
                script += f"Alw-card:loc={loc}\n\n"

            elif action == "delete":
                script += f"inh-card:loc={loc}\n"
                script += f"DLT-IP-HOST:HOST=ipsm{loc}\n"
                script += f"CHG-IP-CARD:LOC={loc}:DEFROUTER=0.0.0.0\n"
                script += f"CHG-IP-LNK:PORT=A:IPADDR=0.0.0.0:LOC={loc}:\n"
                script += f"DLT-CARD:LOC={loc}\n\n"

        elif script_type == "mcpm": 
            if action == "config":
                script += f"ENT-CARD:loc={loc}:TYPE=SLIC:APPL=mcp\n"
                script += f"CHG-IP-LNK:PORT=A:SUBMASK=255.255.255.0:MCAST=YES:IPADDR={ip_a}:LOC={loc}:DUPLEX=FULL:SPEED=100\n"
                script += f"ENT-IP-HOST:HOST=mcpm{loc}:ipaddr={ip_a}\n"
                script += f"CHG-IP-CARD:LOC={loc}.com:DEFROUTER={'.'.join(ip_a.split('.')[:3]) + '.1'}\n"
                script += f"Alw-card:loc={loc}\n\n"

            elif action == "delete":
                script += f"inh-card:loc={loc}\n"
                script += f"DLT-IP-HOST:HOST=mcpm{loc}\n"
                script += f"CHG-IP-CARD:LOC={loc}:DEFROUTER=0.0.0.0\n"
                script += f"CHG-IP-LNK:PORT=A:IPADDR=0.0.0.0:LOC={loc}:\n"
                script += f"DLT-CARD:LOC={loc}\n\n"

        elif script_type == "flash": 
            if action == "flash":
                script += f"INH-CARD:loc={loc}\n"
                script += f"pause 15\n"
                script += f"INIT-FLASH:CODE=APPR:GPL={ip_a}:LOC={loc}\n"
                script += f"pause 150\n"
                script += f"ACT-FLASH:LOC={loc}\n"
                script += f"pause 120\n"
                script += f"Alw-card:loc={loc}\n\n"
    return script

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    action = data.get("action")
    locations = data.get("locations")
    script_type=data.get("scriptType")
    script = generate_script(locations, action, script_type)
    filename = f"{action}_script.txt"
    with open(filename, "w") as file:
        file.write(script)
    return jsonify({"filename": filename})

@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Get PORT from Render, default to 5000 for local testing
    app.run(host="0.0.0.0", port=port, debug=True)
from flask import Flask, render_template, request
import ipaddress

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = {}
    if request.method == 'POST':
        ip = request.form['ip']
        mask = request.form['mask']
        try:
            network = ipaddress.ip_network(f'{ip}/{mask}', strict=False)
            result['network'] = str(network.network_address)
            result['broadcast'] = str(network.broadcast_address)
            result['num_hosts'] = network.num_addresses - 2  # Hosts útiles
            result['range'] = f'{network[1]} - {network[-2]}'
            result['class'] = get_ip_class(ip)
            result['private'] = 'Privada' if network.is_private else 'Pública'
            result['network_bin'] = bin(int(network.network_address)).lstrip('0b').zfill(32)
            result['host_bin'] = bin(int(network.hostmask)).lstrip('0b').zfill(32)
        except ValueError:
            result['error'] = 'Por favor, ingrese una IP y máscara válidas.'

    return render_template('index.html', result=result)

def get_ip_class(ip):
    first_octet = int(ip.split('.')[0])
    if first_octet <= 126:
        return 'Clase A'
    elif first_octet <= 191:
        return 'Clase B'
    elif first_octet <= 223:
        return 'Clase C'
    elif first_octet <= 239:
        return 'Clase D'
    else:
        return 'Clase E'

if __name__ == '__main__':
    app.run(debug=True)


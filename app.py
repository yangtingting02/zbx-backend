from flask import Flask, jsonify, request
from pyzabbix import ZabbixAPIException
from flask_cors import CORS, cross_origin
from zabbix.client import zabbix_client
from conf import config
from zabbix.functools import get_host, filter_group_info, \
    filter_item_info, filter_templates_info


app = Flask(__name__)
CORS(app)


@app.route('/hosts')
def hosts():
    data = zabbix_client.host.get(output="extend")
    hosts = list(map(get_host, data))
    return jsonify({'status': 'success',
                    'data': hosts})


@app.route('/templates')
def templates():
    data = zabbix_client.template.get(output="extend")
    templates = list(map(filter_templates_info, data))
    return jsonify({
        'status': 'success',
        'data': templates
    })


@app.route('/templates/<hostid>')
def liked_templates(hostid):
    ip = zabbix_client.hostinterface.get(output="extend", hostids=hostid)[0]['ip']
    data = zabbix_client.template.get(output="extend", hostids=hostid)
    ltmp = list(map(filter_templates_info, data))
    return jsonify({
        'status': 'success',
        'linked-template': ltmp,
        'ip': ip
    })


@app.route('/template/add', methods=['POST'])
def create_template():
    data = request.get_json()
    templates = data['templates']
    hosts = data['hosts']
    try:
        zabbix_client.template.massadd(templates=templates, hosts=hosts)
        return jsonify({'status': 'success'})
    except ZabbixAPIException as e:
        print(e)
        return jsonify({'status': 'error'})


@app.route('/template/remove', methods=['POST'])
def delete_template():
    data = request.get_json()
    templateids = data['templateids']
    hostids = data['hostids']
    zabbix_client.template.massremove(templateids=templateids, hostids=hostids)
    return jsonify({'status': 'success'})


@app.route('/items')
def items():
    data = zabbix_client.item.get(output="extend")
    ims = list(map(filter_item_info, data))
    return jsonify({
        'status': 'success',
        'items': ims
    })


@app.route('/items/<hostid>')
def host_items(hostid):
    data = zabbix_client.item.get(output="extend", hostids=hostid)
    ip = zabbix_client.hostinterface.get(output="extend", hostids=hostid)[0]['ip']
    ims = list(map(filter_item_info, data))
    return jsonify({
        'status': 'success',
        'items': ims,
        'ip': ip
    })


@app.route('/group/<hostid>')
def group(hostid):
    data = zabbix_client.hostgroup.get(output="extend", hostids=hostid)
    h = zabbix_client.host.get(output="extend", hostids=hostid)
    host = list(map(get_host, h))
    g = list(map(filter_group_info, data))
    return jsonify({
        'status': 'success',
        'group': g,
        'host': host
    })


@app.route('/host/<hostid>/items/<itemid>')
def get_item_history(hostid, itemid):
    item_history = zabbix_client.history.get(output='extend',
                                             history=0,
                                             hostids=hostid,
                                             itemids=itemid,
                                             sortfield='clock',
                                             sortorder='DESC',
                                             limit=50)
    return jsonify({
        'status': 'success',
        'data': item_history
    })


if __name__ == '__main__':
    debug = False if config.env == 'prod' else True
    app.run(debug=debug)



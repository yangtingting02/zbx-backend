from zabbix.client import zabbix_client


def get_host(data):
    ip = zabbix_client.hostinterface.get(output="extend",
                                         hostids=data['hostid'])[0]['ip']
    res = {
        'hostname': data['name'],
        'hostid': data['hostid'],
        'ip': ip
    }
    return res


def filter_templates_info(data):
    res = {
        'template_name': data['name'],
        'templateid': data['templateid']
    }
    return res


def filter_item_info(data):
    res = {
        'key': data['key_'],
        'name': data['name'],
        'itemid': data['itemid'],
        'delay': data['delay'],
        'history': data['history'],
        'trends': data['trends']
    }
    return res


def filter_group_info(data):
    res = {
        'goupid': data['groupid'],
        'name': data['name']
    }
    return res

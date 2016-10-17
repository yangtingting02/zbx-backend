from pyzabbix import ZabbixAPI
from conf import config

zabbix_client = ZabbixAPI(config.zabbix_url)
zabbix_client.login(config.zabbix_username, config.zabbix_password)

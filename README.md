##ZBX,一个简易的zabbix管理系统的后端部分，前端请戳[zbx-app](https://github.com/yangtingting02/zbx-app)。

###运行
- 获取代码
```
git clone git@github.com:yangtingting02/zbx-backend.git
```
- 安装依赖
```
pip install -r requirements.txt
```
- 运行
```
python app.py
```
- 访问
```
curl localhost:5000
```

###功能
这是简易zabbix管理系统后端部分，提供API
####host
```
/hosts
```
####template
```
/templates
```
```
/templates/<hostid>
```
```
/template/add
```
```
/template/remove
```
####item
```
/items
```
```
/items/<hostid>
```
####history
```
/host/<hostid>/items/<itemid>
```



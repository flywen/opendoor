# OpenDoor系统部署说明
## 一、安装操作系统

配置IP，修改时区等等

## 二、环境安装

### 1、安装git
```
$sudo apt-get install git
```
### 2、安装pip
```
$sudo apt-get install python-pip
```
### 3、安装django1.8.6
```
$pip install django==1.8.6
```
### 4、安装nginx
```
$sudo apt-get install nginx
```
### 5、安装uwsgi
```
$sudo apt-get install python-dev
$sudo pip install uwsgi
```
## 三、程序部署
### 1、程序下载
```
$git clone https://github.com/flywen/opendoor.git
```
### 2、修改nginx配置文件
```
server {
        listen 8001;
	
 	location / {
                include uwsgi_params;
                uwsgi_pass 127.0.0.1:9090;		
	}
}
```
### 3、创建、修改uwsgi配置文件
```
[uwsgi]
vhost = false
socket = 127.0.0.1:9090
master = true
enable-threads = true
workers = 6
wsgi-file = /home/pi/opendoor/opendoor/wsgi.py
chdir = /home/pi/opendoor
daemonize = /home/pi/opendoor/visitor.log
disable-logging = true
```
### 4、设置程序自启，修改/etc/rc.local，增加以下内容
```
su pi -c "wsgi /home/pi/opendoor/uwsgi.ini"
```

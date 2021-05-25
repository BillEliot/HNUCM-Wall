# Tech Stack

* Vue@2.6.12
* Nuxt@5.12.5
* ant-design-vue@1.6.5
* Django@3.1.7
* Nginx@1.10.3

# HOW TO START

> dev

```
cd frontend && npm install
npm run dev

cd backend && python3 manager.py runserver
```

> product

## Deploy frontend

```
cd frontend && npm run build
zip -r frontend.zip .nuxt static nuxt.config.js package.json
scp frontend.zip username@address:/var/www/wall/frontend

unzip frontend.zip

npm install
npm install -g pm2
pm2 start npm --name "wall" -- run start
```

## Deploy nginx
```
vim /etc/nginx/nginx.conf

# add
http{
    ...
    # comment
    #include /etc/nginx/conf.d/*.conf;
    #include /etc/nginx/sites-enabled/*;

    upstream wall {
        server 127.0.0.1:3000;
    }

    server{
        listen 80;

        server_name hnucmwall.top;
        index index.html index.htm index.php default.html default.htm default.php;
        location / {
                proxy_set_header X-Real-Ip $remote_addr;
                proxy_set_header X-Forward-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Nginx-Proxy true;
                proxy_pass http://wall;
                proxy_redirect off;
        } 
        location ~ /\.
        {
            deny all;
        }

        access_log  /var/log/nginx/wall.log;
    }

    server{
        listen 8000;
        server_name localhost;
        charset utf-8;
        access_log off;
        location /media {
            alias /var/www/wall/backend/media;
        }
        location / {
            uwsgi_pass  127.0.0.1:8001;
            include     /etc/nginx/uwsgi_params;
            client_max_body_size 300M;
        }
    }
}

service nginx restart
```

## Deploy Backend
```
zip -r backend.zip backend
scp backend.zip username@address:/var/www/wall/backend

unzip backend.zip

pip3 install uwsgi
touch socket.xml && vim socket.xml

<uwsgi>
    <socket>:8001</socket>
    <chdir>.</chdir>
    <module>backend.wsgi:application</module>
    <processes>4</processes>
    <daemonize>uwsgi.log</daemonize>
</uwsgi>

service nginx restart
killall -9 uwsgi
uwsgi -x socket.xml
```

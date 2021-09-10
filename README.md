# Sextic Arm
This project aims to build a 6 degree-of-freedom robot arm which is able to move to any given position and angle using inverse kinematics.

## Installation
### web server
The web server runs on Flask, gunicorn and nginx.
In `/etc/nginx/nginx.conf` or other included `.conf` file, add

    server {
        listen <PORTNUM>;
        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
        
where \<PORTNUM\> is the desired port to listen on.
Then start nginx server by

    sudo nginx
    
to pass http requests to the gunicorn server.

In `SexticArm/web`, run

    gunicorn main:app

It is recommended to write a bash script to autostart everything.

## Documentation
[docs](docs/6DOF.pdf)
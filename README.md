# dummy

####To RUN
docker-compose -f Docker-compose.yaml up --scale sensor=8

Open http://127.0.0.1:8000

Controller.py - async udp server

manipulator.py - simple socket TCP server

webserver.py - flask server

sensor.py - UDP client


![](https://github.com/leonVrashitov/dummy/images/example.png)
![](https://github.com/leonVrashitov/dummy/images/docker.png)
![](https://github.com/leonVrashitov/dummy/images/schema.png)
![](https://github.com/leonVrashitov/dummy/images/controller.png)

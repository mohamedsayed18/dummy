# dummy

### To RUN
```bash	
docker-compose -f Docker-compose.yaml up --scale sensor=8
```

Open http://localhost:8000

* **Controller.py** - async udp server

* **manipulator.py** - simple socket TCP server

* **webserver.py** - flask server

* **sensor.py** - UDP client

### Example
![](https://github.com/leonVrashitov/dummy/blob/master/images/example.png)

### Docker schema
![](https://github.com/leonVrashitov/dummy/blob/master/images/docker.png)

### Netmap
![](https://github.com/leonVrashitov/dummy/blob/master/images/schema.png)

### Controller 
![](https://github.com/leonVrashitov/dummy/blob/master/images/controller.png)

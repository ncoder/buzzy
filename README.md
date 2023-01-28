# howto

control the robot:
(find it's ip address using the arp tool below)
navigate to
```txt
http://(ip):8080
```

# local development of website
start a local server (from the www folder)

```sh
cd www
www> http-server . -c-1
```


navigate to 
```txt
http://localhost:8080/?connectTo=(ip):8080
```

# fullstack local development
just run the python server (instead of http-server) (it serves the website)
configure the environment to forward io ports to the robot.
(todo)

# useful commands

## find buzzy on the local network:
```sh 
arp -a
```

instead of using ip, try
"raspberrypi.lan" hostname.

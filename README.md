# howto

control the robot:
(find it's ip address using the arp tool below)
navigate to
```txt
http://(ip):8080
```

# last configuration options
Buzzy is set to connect to HiperHenri_2.5Ghz
dns on trendnet assigned ip of 192.168.10.101
hostname of buzzy


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

tips: try with a wire. make sure the LNK (flashing) and 100 leds are on.
If using a wire to the extender in the kitchen, connect to HouseOfHenri_ExtB. 
If you don't see the device, disconnect and reconnect hte cable, that sends another arp update.

instead of using ip, try
"raspberrypi.lan" hostname.

# deploy new code to device
```
ssh h@raspberrypi.lan
(use password: password)
cd buzzy
git pull

(restart the server if needed) (how?)
# Timelapse

Take a timelapse from a RTSP stream.

## Install instructions

Deploy with docker compose. The second service enables a network share and is optional.

```yaml
version: "3"

volumes:
  data:

services:
  server:
    image: docker.io/mkomon/timelapse:latest
    container_name: timelapse
    environment:
      - TIMELAPSE_DATA_DIR=/data
      - TIMELAPSE_PERIOD=300
    command: timelapse rtsp://<<VIDEO STREAM URL>>
    restart: always
    volumes:
      - data:/data

  share:
    image: dperson/samba:latest
    container_name: samba
    restart: always
    volumes:
      - data:/data
    command: '-s "timelapse;/data;yes;no;no;timelapse" -u "timelapse;timelapse" -p'
    ports:
      - "137:137/udp"
      - "138:138/udp"
      - "139:139"
      - "445:445"
```

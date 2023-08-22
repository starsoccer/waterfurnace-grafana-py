Original Source for credit: https://gist.github.com/ytjohn/8f65f66693a4105f9aeff13357ab76c1

I have an exporter (python below) that exposes metrics in prometheus format. That puts it into the default datasource of "inlfux".

screenshots:  https://imgur.com/a/xBpfEDY


A second datasource is called weather-influx, which comes from my weatherstation, passed in through http://www.weewx.com/ - but
but if you don't have a weatherstation or weewx, you can find another way to get outside temps into influxdb. Otherwise, you can
remove that outTemp_F stat.


requirements.txt (pip install):
```
prometheus_client
waterfurnace
```

To start, I use a shell script:

```shell
#!/bin/bash

WF_USERNAME="email@example.net"
WF_PASSWORD="password"
WF_UNIT="00M4C0FUN1T"

export WF_USERNAME
export WF_PASSWORD
export WF_UNIT

cd /opt/waterfurnace
/opt/waterfurnace/bin/python waterfurnaceexporter.py
```

I'm using telegraf to dump these into influxdb with its prometheus input.  

```
# Read metrics from one or many prometheus clients
[[inputs.prometheus]]
  ## An array of urls to scrape metrics from.
  urls = ["http://inveigh:8912"]
```

In weewx.conf

```
[StdRESTful]
    [[Influx]]
        host = inveigh
        database = weather
        tags = station=stthomas
```
 
        
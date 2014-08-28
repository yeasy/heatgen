heatgen
=======

A useful tool to generate heat template in JSON format


#Install
Download the latest version and install.
```
git clone https://github.com/yeasy/heatgen.git && sudo bash 
./heatgen/util/install.sh
```

#Usage
After the installation, start heatgen with
```
heatgen --src net_int1 --dst net_int2 --services trans_mb,routed_mb --config-dir
 /etc
```

This will generate a heat template using the sample configuration, 
which has the  following rules
```
net_int1 --> tran_mb --> routed_mb --> net_int2
```

Upgrade

If you wanna upgrade heatgen from a previous version, just run

sudo bash ./heatgen/util/install.sh -u

#Features
* Support automatically deploy the generated templates

#Credits
Thanks to the [OpenStack](http://openstack.org) Heat Team, 
who has written helpful documents on Heat.

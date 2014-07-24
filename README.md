heatgen
=======

A useful tool to generate heat template


##Usage
```
python generator.py --src net_int1 --dst net_int2 --services trans_mb,routed_mb --config-dir etc
```

This will generate a heat template of the following rules

net_int1 --> tran_mb --> routed_mb --> net_int2

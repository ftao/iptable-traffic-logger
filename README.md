# iptable-traffic-logger
Using iptables log traffic for certain port 

## how to use 

enable port traffic logging
```
./tlg.sh enable <PORT>
```

disable port traffic logging
```
./tlg.sh disable <PORT>
```

show and reset port traffic stats
```
./tlg.sh show <PORT>
```


## Radius Support 

1. install dictionary files

    ```
    sudo apt-get install libradius1
    ```
    
2. install required python packages 

    ```
    pip install -r requirements.txt
    ```
    
3. pipe tlg.sh result to  send2radius script to send the acct data to radius server 
    
    ```
    ./tlg.sh show 3456 | python send2radius.py radius.server.address radius-secret 
    ```


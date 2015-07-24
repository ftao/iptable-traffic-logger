#!/bin/bash
ACTION=$1
PORT=$2
IPTABLES=/sbin/iptables
CHAIN_NAME_INPUT="TLG-IN-$PORT"
CHAIN_NAME_OUTPUT="TLG-OUT-$PORT"

function disable(){
    #clear up
    $IPTABLES -D INPUT -p tcp --dport $PORT -j $CHAIN_NAME_INPUT  2>/dev/null
    $IPTABLES -D OUTPUT -p tcp --sport $PORT -j $CHAIN_NAME_OUTPUT 2>/dev/null
    $IPTABLES -F $CHAIN_NAME_INPUT 2>/dev/null
    $IPTABLES -X $CHAIN_NAME_INPUT 2>/dev/null
    $IPTABLES -D $CHAIN_NAME_INPUT 2>/dev/null
    $IPTABLES -F $CHAIN_NAME_OUTPUT 2>/dev/null
    $IPTABLES -X $CHAIN_NAME_OUTPUT 2>/dev/null
    $IPTABLES -D $CHAIN_NAME_OUTPUT 2>/dev/null
}

function enable(){
    disable
    $IPTABLES -N $CHAIN_NAME_INPUT
    $IPTABLES -N $CHAIN_NAME_OUTPUT
    $IPTABLES -A INPUT -p tcp --dport $PORT -j $CHAIN_NAME_INPUT
    $IPTABLES -A OUTPUT -p tcp --sport $PORT -j $CHAIN_NAME_OUTPUT
    $IPTABLES -A $CHAIN_NAME_INPUT
    $IPTABLES -A $CHAIN_NAME_OUTPUT
}

function show(){
    in_bytes=`$IPTABLES -L $CHAIN_NAME_INPUT -Z -vnx | tail -2 | head -1 | awk '{print $2}'`
    out_bytes=`$IPTABLES -L $CHAIN_NAME_OUTPUT -Z -vnx | tail -2 | head -1 | awk '{print $2}'`
    echo "[$in_bytes,$out_bytes]"
}



case "$ACTION" in
    enable)
        echo "setup stats capture rule for $PORT"
        enable
        echo "done"
        ;;
    disable)
        echo "remove stats capture rule for $PORT"
        disable
        echo "done"
        ;;
    show)
        show
        ;;
esac

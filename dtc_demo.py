#!/usr/bin/env python3
import socket, json, threading, time

HOST = "10.211.55.3"   # <-- your Windows VM IP (ipconfig). Not 127.0.0.1 on macOS.
PORT = 12000           # DTC live port is 11099 but we need the proxy here.
SYMBOL = "ESU5.CME"  # ESU5.CME (must use Rhithnmic; Denali won't work except on localhost due to exchange rules).
SYMBOL_ID = 1        # anything you want.

HEARTBEAT_SEC = 5

def send(sock, obj):
    data = (json.dumps(obj) + "\x00").encode("utf-8")
    sock.sendall(data)

def heartbeat_loop(sock, stop_event):
    # DTC heartbeat: Type = 3
    while not stop_event.is_set():
        time.sleep(HEARTBEAT_SEC)
        try:
            send(sock, {"Type": 3})
        except Exception:
            break

def main():
    with socket.create_connection((HOST, PORT), timeout=5) as sock:
        # LOGON_REQUEST (Type 1). Keep it small and standards-compliant.
        send(sock, {
            "Type": 1,  # LOGON_REQUEST
            "HeartbeatIntervalInSeconds": HEARTBEAT_SEC,
            "ClientName": "SimpleDTCClient"
            # "ProtocolVersion": 8,       # optional; server will set it
            # "Username": "", "Password": ""  # only if you enabled auth
        })

        # Start heartbeat thread
        stop = threading.Event()
        hb = threading.Thread(target=heartbeat_loop, args=(sock, stop), daemon=True)
        hb.start()

        # Subscribe to market data (Type 101)
        send(sock, {
            "Type": 101,               # MARKET_DATA_REQUEST
            "RequestAction": "Subscribe",
            "SymbolID": SYMBOL_ID,
            "Symbol": SYMBOL,
            "Exchange": ""             # leave blank unless you know it
        })

        # Print each JSON message (delimited by NUL)
        buf = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            buf += chunk
            while b"\x00" in buf:
                raw, buf = buf.split(b"\x00", 1)
                if not raw:
                    continue
                try:
                    msg = json.loads(raw.decode("utf-8"))
                    print(msg)
                except Exception as e:
                    print("Bad frame:", raw[:200], e)

        stop.set()
        hb.join(timeout=1)

if __name__ == "__main__":
    main()

def lire(file_path : str) :
    with open(file_path, 'r') as file:
        for line in file:
            a=line.strip()
            if a:
                yield a

def lire_tout(file_path : list[str]) :
    for p in file_path:
        yield from lire(p)

import json

def parsing_des_log(line):
    parts = line.split(" ", maxsplit=5)
    
    if len(parts) < 5:
        return {"raw": line, "type": "malformed"}
    
    timestamp = parts[0] + " " + parts[1]
    severity = parts[2]
    ip_address = parts[3]
    rest = parts[4].split(" ", maxsplit=1)
    if len(rest) > 1 :
        user_id = rest[0]
    else :
        user_id = None
    if len(rest) > 1:
     message_content = rest[1]  
    else :
        message_content = None
    
    network_meta = (ip_address, 443, "HTTPS")


    return {
        "timestamp": timestamp,
        "severity": severity,
        "ip": ip_address,
        "user_id": user_id,
        "message": message_content,
        "network_meta": network_meta
    }


def module_1(file_paths):
    for line in lire_tout(file_paths):
        yield parsing_des_log(line)
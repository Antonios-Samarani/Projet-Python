def lire(file_path : str) :
    with open(file_path, 'r') as file:
        for line in file:
            a=line.strip()
            if a:
                yield a

def lire_tout(file_path : list[str]) :
    for p in file_path:
        yield from p.lire()

import json

def parsing_des_log(line):
    parts = line.split(" ", maxsplit=5)
    
    if len(parts) < 5:
        return {"raw": line, "type": "malformed"}
    
    timestamp = f"{parts[0]} {parts[1]}"
    severity = parts[2]
    ip_address = parts[3]
    rest = parts[4].split(" ", maxsplit=1)
    user_id = parts[5]
    message_content = parts[6]

    


    return {
        "timestamp": timestamp,
        "severity": severity,
        "ip": ip_address,
        "user_id": user_id,
        
    }


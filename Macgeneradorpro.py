
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, random, time

OUI_LIST=[
"00:1A:2B","00:1C:42","00:1D:70","00:0A:95","00:1B:63",
"00:16:3E","00:25:96","00:50:56","08:00:27","3C:5A:B4",
"AC:DE:48","B8:27:EB","DC:A6:32","F4:F5:D8","D8:CB:8A",
"70:85:C2","E0:91:F5","5C:F9:38","FC:FB:FB","40:B0:34"
]
DEST="/storage/emulated/0/combos"
if not os.path.isdir("/storage/emulated/0"):
    DEST="combos"

def gen():
    oui=random.choice(OUI_LIST)
    return oui+":"+":".join(f"{random.randint(0,255):02X}" for _ in range(3))

def cisco(mac):
    s=mac.replace(":","")
    return f"{s[:4]}.{s[4:8]}.{s[8:]}"

def clear():
    os.system("cls" if os.name=="nt" else "clear")

def panel(done,total,name,start,dups,fmt):
    clear()
    pct=done/total if total else 0
    width=36
    fill=int(width*pct)
    bar="█"*fill+"░"*(width-fill)
    elapsed=time.time()-start
    speed=done/elapsed if elapsed>0 else 0
    eta=(total-done)/speed if speed>0 else 0
    print("╔"+"═"*58+"╗")
    print("║           MAC GENERATOR PRO FOR QPYTHON               ║")
    print("╚"+"═"*58+"╝")
    print(f"Archivo : {name}")
    print(f"Destino : {os.path.abspath(DEST)}")
    print(f"\n[{bar}] {pct*100:5.1f}%")
    print(f"Generadas : {done}/{total}")
    print(f"Duplicados: {dups}")
    print(f"Velocidad : {speed:,.0f} MAC/s")
    print(f"Tiempo    : {elapsed:.1f}s")
    print(f"ETA       : {eta:.1f}s")
    print(f"Formato   : {fmt}")

while True:
    clear()
    print("=== MAC GENERATOR PRO ===")
    name=input("Nombre del archivo (sin extension): ").strip() or "macs"
    try:
        total=int(input("Cantidad de MACs: "))
        if total<=0: raise ValueError
    except:
        input("Cantidad invalida. ENTER...")
        continue
    op=input("Formato 1)Estandar 2)Cisco [1]: ").strip() or "1"
    fmt="Cisco" if op=="2" else "Standard"
    os.makedirs(DEST,exist_ok=True)
    path=os.path.join(DEST,name+".txt")
    seen=set(); dups=0
    start=time.time()
    with open(path,"w") as f:
        while len(seen)<total:
            m=gen()
            if op=="2": m=cisco(m)
            if m in seen:
                dups+=1
                continue
            seen.add(m)
            f.write(m+"\n")
            if len(seen)%250==0 or len(seen)==total:
                panel(len(seen),total,name+".txt",start,dups,fmt)
    size=os.path.getsize(path)/1024
    clear()
    print("Proceso finalizado\n")
    print("Archivo :",path)
    print("MACs    :",len(seen))
    print("Duplicados:",dups)
    print("Tiempo  : %.2fs"%(time.time()-start))
    print("Tamano  : %.1f KB"%size)
    if input("\nGenerar otro? (S/N): ").lower() not in ("s","si","y","yes"):
        break

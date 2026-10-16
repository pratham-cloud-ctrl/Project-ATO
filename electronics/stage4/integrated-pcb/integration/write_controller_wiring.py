"""Bind the actual carrier headers to frozen circuit connector pins."""
import csv,json,re,xml.etree.ElementTree as ET
from build_integration import ROOT,STAGE,PACKAGES,MAINS
def main():
    lookup={};by_net={}
    for pkg,name in zip(PACKAGES,MAINS):
        x=ET.parse(STAGE/pkg/(name+'.xml')).getroot()
        for n in x.findall('nets/net'):
            for p in n.findall('node'):
                lookup[pkg,p.get('ref'),p.get('pin')]=n.get('name')
                if p.get('ref').startswith('J'):by_net.setdefault((pkg,n.get('name')),[]).append((p.get('ref'),p.get('pin')))
    rows=[];seen=set()
    def add(cref,cpin,pkg,ref,pin,purpose):
        signature=(cref,str(cpin),pkg,ref,str(pin))
        if signature in seen:return
        seen.add(signature)
        rows.append({'from_package':'controller-carrier','from_ref':cref,'from_pin':str(cpin),'from_net':lookup['controller-carrier',cref,str(cpin)],'to_package':pkg,'to_ref':ref,'to_pin':str(pin),'to_net':lookup[pkg,ref,str(pin)],'purpose':purpose})
    pinrows=list(csv.DictReader((ROOT/'docs/stage4/nrf5340-pin-map.csv').open(encoding='utf-8-sig')))
    endpoints=0
    for r in pinrows:
        for connection in r['connection'].split(';'):
            m=re.fullmatch(r'([^:]+):(J[0-9]+)\.([0-9]+)',connection)
            if not m:continue
            pkg,ref,pin=m[1],m[2],int(m[3]);endpoints+=1
            if pkg=='recording-front-end':cr,cp='J11',pin
            elif pkg=='monitoring-transport' and ref=='J3':cr,cp='J10',pin
            elif pkg=='monitoring-transport' and ref=='J22':cr,cp='J12',pin
            elif pkg=='monitoring-transport' and ref=='J20':cr,cp='J13',pin-7
            elif pkg=='monitoring-transport' and ref=='J7':cr,cp='J20',pin
            elif pkg=='current-driver' and ref=='J2':cr,cp='J14',pin
            elif pkg=='current-driver' and ref=='J3':cr,cp='J15',pin
            elif pkg=='contact-router' and ref=='J2':cr,cp='J16',pin
            elif pkg=='contact-router' and ref=='J3':cr,cp='J16',pin+6
            elif pkg=='contact-router' and ref=='J4':cr,cp='J16',6
            elif pkg=='supervision' and ref=='J3':cr,cp='J18',(pin if pin<10 else pin-4)
            else:raise AssertionError(connection)
            assert lookup['controller-carrier',cr,str(cp)]==r['signal'],(r,cr,cp)
            add(cr,cp,pkg,ref,pin,'Compiled firmware '+r['pin']+' '+r['signal']+' physical header binding')
    # Explicit return/supply pins for each loom, never an assumed common label.
    for cr,cp,pkg,ref,pin in [
        ('J1',1,'power','J3',3),('J1',2,'power','J3',7),
        ('J10',6,'monitoring-transport','J3',6),
        ('J11',1,'recording-front-end','J2',1),('J11',2,'recording-front-end','J2',2),('J11',10,'recording-front-end','J2',10),
        ('J12',7,'monitoring-transport','J22',7),('J13',5,'monitoring-transport','J20',12),
        ('J14',4,'current-driver','J2',4),('J15',9,'current-driver','J3',9),
        ('J16',9,'contact-router','J2',7),('J17',9,'contact-router','J6',9),
        ('J18',8,'supervision','J3',12),('J19',19,'supervision','J5',13),
        ('J20',3,'monitoring-transport','J7',3),('J20',4,'monitoring-transport','J7',4)]:
        expected='HOST_3V3' if (cr,cp) in [('J1',1),('J11',1),('J20',3)] else 'GND'
        actual=lookup[pkg,ref,str(pin)]
        assert actual in ([expected,'HOSTGND'] if expected=='GND' else [expected]),(cr,cp,pkg,ref,pin,actual)
        add(cr,cp,pkg,ref,pin,'Actual host-side harness supply/return; AFEAGND and COMP_GND remain separate')
    for pin in range(1,9):add('J17',pin,'contact-router','J6',pin,'Actual active-latch address readback to 165 sample bit '+str(pin-1))
    carrier=json.loads((STAGE/'controller-carrier/connectivity.json').read_text(encoding='utf-8'))
    for pin,signal in carrier['harnesses']['J19']['nets'].items():
        if signal=='GND':continue
        pkg='power' if signal=='PWR_FAULT_N' else ('current-driver' if signal in ['CH0_RUN','CH1_RUN','CH0_TIMER','CH1_TIMER','CH0_TIMEOUT','CH1_TIMEOUT'] else ('contact-router' if signal=='ROUTE_COMMAND_READY' else 'supervision'))
        candidates=by_net[pkg,signal]
        assert candidates,(pkg,signal)
        ref,p=candidates[0]
        add('J19',pin,pkg,ref,p,'Native observed '+signal+' to serialized health bit '+str(int(pin)+7))
    path=ROOT/'docs/stage4/integrated-pcb-controller-wiring.csv'
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    print(json.dumps({'firmware_endpoint_bindings':endpoints,'carrier_wires':len(rows),'path':str(path)}))
if __name__=='__main__':main()

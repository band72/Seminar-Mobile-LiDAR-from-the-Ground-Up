import numpy as np
d=np.deg2rad; R=152.4; FT=0.3048
imus={'RiLOC-F':(0.005,0.005,0.025),'AP+30':(0.010,0.025,0.035),'AP+50':(0.005,0.010,0.035),'AP+60':(0.0025,0.005,0.035)}
# (rp deg, heading deg, gnss H m (vertical = 1.5x)) using datasheet position 0.02-0.03 (RiLOC) /0.02-0.05 AP
sr_acc=0.020; sr_prec=0.015; sr=np.hypot(sr_acc,sr_prec)
bs=d(0.005); lev=0.005; enc=d(0.001)/np.sqrt(12)
print("range total",sr, "enc",R*enc)
for name,(rp,hd,gH) in imus.items():
  gV=1.5*gH
  for th_deg in (0,37.5):
    th=d(th_deg)
    terms_h={'GNSS':gH,'roll/pitch':np.hypot(R*np.cos(th)*d(rp), R*np.cos(th)*d(rp)) if th_deg>0 else np.hypot(R*d(rp),R*d(rp)),
             'heading':R*np.sin(th)*d(hd),'range':sr*np.sin(th),'boresight':np.sqrt((R*np.cos(th)*bs)**2*2+(R*np.sin(th)*bs)**2),'lever':lev*np.sqrt(2),'encoder':R*np.cos(th)*enc}
    terms_v={'GNSS':gV,'roll':R*np.sin(th)*d(rp),'range':sr*np.cos(th),'boresight':R*np.sin(th)*bs,'lever':lev,'encoder':R*np.sin(th)*enc}
    H=np.sqrt(sum(v*v for v in terms_h.values())); V=np.sqrt(sum(v*v for v in terms_v.values()))
    print(name,th_deg,"H",round(H*100,2),"cm",round(H/FT,3),"ft | V",round(V*100,2),"cm",round(V/FT,3),"ft")
    print("   h:",{k:round(v*100,2) for k,v in terms_h.items()}); print("   v:",{k:round(v*100,2) for k,v in terms_v.items()})
print("angles at 152.4 m (mm):",{a:round(R*d(a)*1000,1) for a in (0.0025,0.005,0.010,0.025)})
print("footprint",0.35e-3*R*1000,"mm")
c=299792458/1.0003
for prr in (300e3,600e3,1200e3,1800e3,2400e3): print(prr, c/(2*prr), R/(c/(2*prr)))
for H in (152.4,): sw=2*H*np.tan(d(37.5)); print("swath",sw, "dens60kn",2e6/(sw*30.87),"dens10ms",2e6/(sw*10))
print("check 1100ft",2e6/(2*335.28*np.tan(d(37.5))*30.87))
print("timing 1ms 60kn",30.87e-3,"10us",30.87e-5)
print("AGL edge",R*np.cos(d(37.5)), R*np.cos(d(37.5))/FT)

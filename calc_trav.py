import numpy as np
d=np.deg2rad
A=np.array([1000.,1000.])
legs=[(200,90),(150,180),(200,270),(150,0)]  # dist, azimuth (deg, clockwise from north)
def trav(legs, dh=None, scale=0.0):
    p=A.copy(); pts=[p.copy()]
    for i,(L,az) in enumerate(legs):
        a=az+(dh[i] if dh is not None else 0)
        Ls=L*(1+scale)
        p=p+Ls*np.array([np.sin(d(a)),np.cos(d(a))]); pts.append(p.copy())
    return np.array(pts)
T=trav(legs); print("true",T)
S=trav(legs,[0.8]*4,0.002); print("sys bias",S, "misclose",S[-1]-A, "B err",S[1]-T[1], np.linalg.norm(S[1]-T[1]), "C err",np.linalg.norm(S[2]-T[2]))
R=trav(legs,[0.8,0.8-2.0,0.8,0.8],0.002); mis=R[-1]-A; print("bridge",R,"mis",mis,np.linalg.norm(mis),"precision 1:",700/np.linalg.norm(mis))
# compass rule adjustment
cum=np.cumsum([0]+[l for l,_ in legs]); adj=R - np.outer(cum/700, mis); print("adjusted",adj, "errs",[np.linalg.norm(adj[i]-T[i]) for i in range(5)])
# MC random heading 0.8 rms independent per leg + odo 0.2% random
rng=np.random.default_rng(3); M=[]
for k in range(20000):
    Rk=trav(legs, rng.normal(0,0.8,4), rng.normal(0,0.002)); M.append(np.linalg.norm(Rk[-1]-A))
M=np.array(M); print("MC misclosure mean",M.mean(),"95%",np.percentile(M,95))
# pure inertial
g=9.80665; t=70
for lab,ba in [("bias instability 0.04mg",0.04e-3*g),("initial bias 2mg",2e-3*g),("tilt 0.25deg",g*np.sin(d(0.25)))]:
    print(lab, ba, 0.5*ba*t*t, "at 20s",0.5*ba*400, "10s",0.5*ba*100)
bg=d(8)/3600; print("gyro 8deg/h 70s heading deg",8/3600*70, "lateral",0.5*10*bg*t*t)
bgi=d(0.04); print("initial gyro bias 0.04deg/s -> 70s heading",0.04*70,"lateral",0.5*10*bgi*t*t)
arw=0.005*60; print("ARW deg/rt h",arw, "70s",arw*np.sqrt(70/3600))
vrw=25e-6*g; print("VRW m/s/rt s",vrw, "pos rw 70s ~", vrw*t**1.5/np.sqrt(3))
# LiDAR point errors
for lab,deg in [("heading 0.8",0.8),("rollpitch 0.25",0.25),("heading 0.5 gnss",0.5)]:
    print(lab, [round(r*d(deg)*100,1) for r in (5,10,20,35)])
# INS point at 20 m total
h=np.sqrt(2**2+ (20*d(0.8))**2 + 0.0131**2); v=np.sqrt(5**2+(20*d(0.25))**2); print("INS total 20m H",h,"V",v)

import numpy as np
np.set_printoptions(precision=5, suppress=True)
d=np.deg2rad
def Rx(a):c,s=np.cos(a),np.sin(a);return np.array([[1,0,0],[0,c,-s],[0,s,c]])
def Ry(a):c,s=np.cos(a),np.sin(a);return np.array([[c,0,s],[0,1,0],[-s,0,c]])
def Rz(a):c,s=np.cos(a),np.sin(a);return np.array([[c,-s,0],[s,c,0],[0,0,1]])
print("== EP2b rho 30")
h=2.0; D=np.sqrt(30**2-4); rho=30.0; V=-np.arcsin(h/rho); H=d(30); sr=0.010; sa=d(0.01)
J=np.array([[np.cos(V)*np.cos(H), -rho*np.cos(V)*np.sin(H), -rho*np.sin(V)*np.cos(H)],
            [np.cos(V)*np.sin(H),  rho*np.cos(V)*np.cos(H), -rho*np.sin(V)*np.sin(H)],
            [np.sin(V), 0, rho*np.cos(V)]]); print("V",np.rad2deg(V),"J",J)
C=J@np.diag([sr**2,sa**2,sa**2])@J.T; print("C mm2",C*1e6,"sig",np.sqrt(np.diag(C))*1000)
w,v=np.linalg.eigh(C); print("eig",np.sqrt(w)*1000, v[:,2])
wh,vh=np.linalg.eigh(C[:2,:2]); print("horiz 1s",np.sqrt(wh)*1000,"95",2.4477*np.sqrt(wh)*1000, "dir major",np.degrees(np.arctan2(vh[1,1],vh[0,1])))
print("xyz",rho*np.cos(V)*np.cos(H),rho*np.cos(V)*np.sin(H),rho*np.sin(V))
# precision curve from datasheet chart (10% target), cm
rr=np.array([1,5,10,15,20,25,30,35.]); pc=np.array([0.25,0.25,0.25,0.28,0.40,0.65,1.0,1.5])
def prec(r): return np.interp(r,rr,pc)/100
print("== georef budget")
sig=dict(pE=0.015,pN=0.015,pU=0.020,roll=d(0.02),pitch=d(0.02),yaw=d(0.05),bs=d(0.01),lev=0.002,racc=0.0125,ang=d(0.01))
l=np.array([0.05,0.0,0.10])
def point(par, rho, H, V):
    p=np.array([par['pE'],par['pN'],par['pU']])
    rs=np.array([rho*np.cos(V)*np.cos(H),rho*np.cos(V)*np.sin(H),rho*np.sin(V)])
    Rbs=Rz(par['bz'])@Ry(par['by'])@Rx(par['bx'])
    Rnb=Rz(d(30)+par['yaw'])@Ry(par['pitch'])@Rx(par['roll'])
    return p+Rnb@(Rbs@rs+l+np.array([par['lx'],par['ly'],par['lz']]))
names=['pE','pN','pU','roll','pitch','yaw','bx','by','bz','lx','ly','lz','rho','H','V']
def budget(rho,H,V,verbose=False):
    base={k:0.0 for k in ['pE','pN','pU','roll','pitch','yaw','bx','by','bz','lx','ly','lz']}
    def f(x):
        par=dict(zip(names[:12],x[:12])); return point(par,x[12],x[13],x[14])
    x0=np.array([0]*12+[rho,H,V],float); eps=1e-7
    Jm=np.array([(f(x0+eps*np.eye(15)[i])-f(x0-eps*np.eye(15)[i]))/(2*eps) for i in range(15)]).T
    sp=prec(rho); srange=np.hypot(sig['racc'],sp)
    s=np.array([sig['pE'],sig['pN'],sig['pU'],sig['roll'],sig['pitch'],sig['yaw'],sig['bs'],sig['bs'],sig['bs'],sig['lev'],sig['lev'],sig['lev'],srange,sig['ang'],sig['ang']])
    C=Jm@np.diag(s**2)@Jm.T
    groups={'trajectory position':[0,1,2],'attitude (IMU/SLAM)':[3,4,5],'boresight':[6,7,8],'lever arm':[9,10,11],'range (acc+prec)':[12],'angle encoders':[13,14]}
    out={}
    for g,idx in groups.items():
        Cg=Jm[:,idx]@np.diag(s[idx]**2)@Jm[:,idx].T; out[g]=(np.sqrt(Cg[0,0]+Cg[1,1]),np.sqrt(Cg[2,2]))
    return C,out,Jm,s,f,x0
for (lab,H,V) in [('wall point to the side, level',d(90),0.0)]:
  for rho in [5,10,20,35]:
    C,out,Jm,s,f,x0=budget(rho,H,V)
    print(lab,rho,"H tot cm",100*np.sqrt(C[0,0]+C[1,1]),"V tot cm",100*np.sqrt(C[2,2]))
    for g,(hh,vv) in out.items(): print("   ",g,round(hh*100,2),round(vv*100,2))
# MC at 20 m
C,out,Jm,s,f,x0=budget(20,d(90),0.0)
rng=np.random.default_rng(5); N=100000
X=x0+rng.standard_normal((N,15))*s
P=np.array([f(x) for x in X]); m=P.mean(0); 
print("MC H",100*np.sqrt(P[:,0].var()+P[:,1].var()),"V",100*P[:,2].std(), "lin H",100*np.sqrt(C[0,0]+C[1,1]),"V",100*np.sqrt(C[2,2]))
np.save('figs/mc_dz.npy',(P[:,2]-f(x0)[2]))
print("prec 20",prec(20),"srange20",np.hypot(0.0125,prec(20)))

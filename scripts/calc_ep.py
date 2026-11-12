import numpy as np
np.set_printoptions(precision=6, suppress=True)
d=np.deg2rad; r2d=np.rad2deg
print("== EP1 height of ground point")
h=2.0; D=20.0; rho=np.hypot(D,h); V=-np.arctan2(h,D); print("rho",rho,"V",r2d(V))
sr=0.0035; sV=d(0.01)
a=np.sin(V)*sr; b=rho*np.cos(V)*sV; print("terms",a,b,"sz",np.hypot(a,b), "sinV",np.sin(V),"cosV",np.cos(V))
print("== EP2 jacobian")
H=d(30)
def xyz(q): r,H,V=q; return np.array([r*np.cos(V)*np.cos(H), r*np.cos(V)*np.sin(H), r*np.sin(V)])
q=np.array([rho,H,V]); print("xyz",xyz(q))
J=np.array([[np.cos(V)*np.cos(H), -rho*np.cos(V)*np.sin(H), -rho*np.sin(V)*np.cos(H)],
            [np.cos(V)*np.sin(H),  rho*np.cos(V)*np.cos(H), -rho*np.sin(V)*np.sin(H)],
            [np.sin(V), 0, rho*np.cos(V)]]); print("J",J)
S=np.diag([sr**2,sV**2,sV**2]); C=J@S@J.T; print("C (mm^2)",C*1e6); print("sig mm",np.sqrt(np.diag(C))*1000)
w,v=np.linalg.eigh(C); print("eig sig mm",np.sqrt(w)*1000)
Ch=C[:2,:2]; wh=np.linalg.eigvalsh(Ch); print("horiz ellipse semi-axes mm 1sig",np.sqrt(wh)*1000,"95%",2.4477*np.sqrt(wh)*1000)
print("3D 95% factor 2.7955 ->", 2.7955*np.sqrt(w)*1000)
# MC
rng=np.random.default_rng(1); N=200000
Q=q+rng.standard_normal((N,3))*np.array([sr,sV,sV]); P=np.array([xyz(x) for x in Q[:20000]])
print("MC sig mm (20k)",P.std(0)*1000)
print("== EP3 correlated difference")
print("random only",np.sqrt(2)*0.25,"cm")
print("== EP4 averaging", 0.25/np.sqrt(400), np.sqrt(1.25**2+(0.25/20)**2))
print("== EP7 volume", 2000*0.0125)

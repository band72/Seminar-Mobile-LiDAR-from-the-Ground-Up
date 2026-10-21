import numpy as np
np.set_printoptions(precision=5, suppress=True)
d=np.deg2rad; r2d=np.rad2deg
print("== Brenner motion")
x,y,th=10.0,5.0,0.0; L,Rr,w=0.40,0.45,0.30
a=(Rr-L)/w; Rt=L/a; k=Rt+w/2
xn=x+k*(np.sin(th+a)-np.sin(th)); yn=y-k*(np.cos(th+a)-np.cos(th)); tn=th+a
print(a, r2d(a), Rt, xn, yn, r2d(tn))
G=np.array([[1,0,k*(np.cos(th+a)-np.cos(th))],[0,1,k*(np.sin(th+a)-np.sin(th))],[0,0,1]]); print("G",G)
P=np.diag([0.01,0.01,0.001]); Q=np.diag([0.002,0.002,0.0005])
GP=G@P@G.T; print("GPG^T",GP); Pb=GP+Q; print("Pbar",Pb, "sig",np.sqrt(np.diag(Pb)), r2d(np.sqrt(Pb[2,2])))
print("== measurement")
xl,yl=25.0,8.0; dx=xl-xn; dy=yl-yn; q=dx*dx+dy*dy; rh=np.sqrt(q); bh=np.arctan2(dy,dx)-tn
print(dx,dy,q,rh,r2d(np.arctan2(dy,dx)),r2d(bh))
z=np.array([14.95,d(2.10)]); inn=z-np.array([rh,bh]); print("innov",inn[0],r2d(inn[1]))
H=np.array([[-dx/rh,-dy/rh,0],[dy/q,-dx/q,-1]]); print("H",H)
Rm=np.diag([0.05**2,d(1)**2]); S=H@Pb@H.T+Rm; print("S",S)
K=Pb@H.T@np.linalg.inv(S); print("K",K)
xs=np.array([xn,yn,tn])+K@inn; print("x+",xs[0],xs[1],r2d(xs[2]))
Pn=(np.eye(3)-K@H)@Pb; print("P+",Pn,"sig",np.sqrt(np.diag(Pn)),r2d(np.sqrt(Pn[2,2])))
print("== 1D Kalman")
K1=0.25/(0.29); print(K1,100+K1*0.4,(1-K1)*0.25,np.sqrt((1-K1)*0.25))
print("== ICP 2D known correspondences")
Pp=np.array([[0,0],[2,0],[2,1],[0,3]],float)
th=d(10); Rtrue=np.array([[np.cos(th),-np.sin(th)],[np.sin(th),np.cos(th)]]); t=np.array([1.0,0.5])
Qq=(Rtrue@Pp.T).T+t; print("Q",Qq)
pb=Pp.mean(0); qb=Qq.mean(0); print("means",pb,qb)
Pc=Pp-pb; Qc=Qq-qb; print("Pc",Pc,"Qc",Qc)
# 2D closed form angle
Sxx=sum(Pc[:,0]*Qc[:,0]+Pc[:,1]*Qc[:,1]); Sxy=sum(Pc[:,0]*Qc[:,1]-Pc[:,1]*Qc[:,0])
ang=np.arctan2(Sxy,Sxx); print("sums",Sxx,Sxy,"angle",r2d(ang))
Re=np.array([[np.cos(ang),-np.sin(ang)],[np.sin(ang),np.cos(ang)]]); te=qb-Re@pb; print("t",te)
Hc=Pc.T@Qc; U,s,Vt=np.linalg.svd(Hc); print("Hcross",Hc,"R svd",Vt.T@U.T)
print("== edge/plane distance")
p=np.array([1.0,0.6,0.8]); A=np.array([0,0,0.]); B=np.array([2,0,0.])
print("edge d",np.linalg.norm(np.cross(p-A,p-B))/np.linalg.norm(A-B), np.cross(p-A,p-B))
u=np.array([0,0,0.]);v=np.array([1,0,0.]);ww=np.array([0,1,0.]); pp=np.array([0.3,0.4,0.12])
nrm=np.cross(u-v,u-ww); print("normal",nrm,"plane d",abs((pp-u)@nrm)/np.linalg.norm(nrm))
print("== LOAM curvature")
r=np.array([10.0,10.0,10.0,10.0,10.0,10.0]) # placeholder

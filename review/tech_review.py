"""Independent recomputation of key numbers printed in the seminar book."""
import math, json, csv
FT=0.3048; d2r=math.radians
rows=[]
def chk(module,item,printed,computed,tol,unit=""):
    ok=abs(printed-computed)<=tol
    rows.append((module,item,printed,round(computed,4),unit,"PASS" if ok else "CHECK"))
c=299792458
chk("M3","Range from 1 us round trip (m)",149.9,c*1e-6/2,0.05,"m")
chk("M3","Max unambiguous range at 1 MHz PRF (m)",149.9,c/(2*1e6),0.05,"m")
chk("M2","Small-angle: 0.1 deg at 100 m (cm)",17.5,100*d2r(0.1)*100,0.05,"cm")
chk("M5","Quantization sigma for q=1 mm (mm)",0.29,1/math.sqrt(12),0.005,"mm")
for cols,p in [(512,0.703),(1024,0.352),(2048,0.176),(4096,0.088)]:
    chk("M15","OS0 horizontal step %d cols (deg)"%cols,p,360/cols,0.0006,"deg")
chk("M15","OS0 1024-col spacing at 10 m (cm)",6.1,10*d2r(360/1024)*100,0.05,"cm")
chk("M15","OS0 1024-col spacing at 35 m (cm)",21.5,35*d2r(360/1024)*100,0.05,"cm")
chk("M15","OS0 128-ch vertical step (deg)",0.709,90/127,0.001,"deg")
chk("M15","OS0 footprint 0.35 deg at 20 m incl. 5 mm exit (cm)",12.7,0.5+20*d2r(0.35)*100,0.05,"cm")
chk("M15","75 m in ft",246,75/FT,0.5,"ft")
rho=500*FT
chk("M14/M17","500 ft in m",152.4,rho,0.001,"m")
for a,p in [(0.0025,0.7),(0.005,1.3),(0.010,2.7),(0.025,6.6)]:
    chk("M14/M17","Attitude %.4f deg at 152.4 m (cm)"%a,p,rho*d2r(a)*100,0.05,"cm")
e=rho*d2r(0.005)*100
chk("M14","RiLOC-F nadir H RSS (cm)",3.7,math.sqrt(2.5**2+2*e**2+2*e**2+0.71**2+0.08**2),0.05,"cm")
chk("M14","RiLOC-F nadir V RSS (cm)",4.5,math.sqrt(3.75**2+2.5**2+0.5**2),0.05,"cm")
s=math.sin(d2r(37.5)); co=math.cos(d2r(37.5)); a=rho*d2r(0.005)*100
rp=math.hypot(a*co,a*co); hd=a*s; bs=math.sqrt((a*co)**2*2+hd**2)
chk("M14","RiLOC-F edge H RSS (cm)",3.9,math.sqrt(2.5**2+rp**2+hd**2+(2.5*s)**2+bs**2+0.71**2),0.06,"cm")
chk("M14","RiLOC-F edge V RSS (cm)",4.4,math.sqrt(3.75**2+hd**2+(2.5*co)**2+hd**2+0.5**2),0.05,"cm")
chk("M14","Timing 1 ms at 60 kn (cm)",3.1,60*1852/3600*1e-3*100,0.05,"cm")
chk("M20","Swath at 400 ft, +/-37.5 deg (m)",187,2*400*FT*math.tan(d2r(37.5)),0.5,"m")
chk("M20","Swath 187 m in ft",614,187/FT,0.5,"ft")
chk("M20","Density 2.0e6 pts/s, 187 m, 10 m/s (pts/m2)",1070,2.0e6/(187*10),3,"pts/m2")
chk("M21","Drive speed limit 0.25 m x 20 Hz x 4 ch (m/s)",20,0.25*20*4,0.01,"m/s")
chk("M21","Outage time 300 m at 13 m/s (s)",23.1,300/13,0.05,"s")
chk("M21","Accel drift 0.5 mg over 23.1 s (m)",1.31,0.5*0.0049*23.1**2,0.01,"m")
chk("M21","Gyro 1 deg/h lateral drift (m)",0.017,0.5*13*d2r(1/3600)*23.1**2,0.001,"m")
st=json.load(open("figs/sample_stats.json"))
dz=[float(r["dZ_cm"]) for r in csv.DictReader(open("figs/sample_checkpoints.csv"))]
chk("M21","Dataset RMSEz from CSV (cm)",1.90,math.sqrt(sum(x*x for x in dz)/len(dz)),0.005,"cm")
chk("M21","Dataset mean dZ (cm)",0.31,sum(dz)/len(dz),0.005,"cm")
chk("M21","Final RMSEz incl. 0.8 cm checkpoint (cm)",2.06,math.hypot(1.90,0.8),0.005,"cm")
chk("M21","RMSE_H data (cm)",2.63,math.hypot(2.00,1.71),0.005,"cm")
rd=list(csv.DictReader(open("figs/sample_checkpoints.csv")))
rx=math.sqrt(sum(float(r["dE_cm"])**2 for r in rd)/30); ry=math.sqrt(sum(float(r["dN_cm"])**2 for r in rd)/30)
chk("M21","Dataset RMSE_x from CSV (cm)",2.00,rx,0.005,"cm")
chk("M21","Dataset RMSE_y from CSV (cm)",1.71,ry,0.005,"cm")
chk("M21","Final RMSE_H incl. 1.0 cm, unrounded (cm)",2.82,math.hypot(math.hypot(rx,ry),1.0),0.005,"cm")
chk("M21","Final RMSE_H in ft",0.092,2.8175/30.48,0.0006,"ft")
chk("M13","ASPRS 95% vertical factor x RMSE 3 cm (cm)",5.88,1.96*3,0.005,"cm")
chk("M13","ASPRS horizontal 95% factor (2-D)",2.448,math.sqrt(-2*math.log(0.05)),0.001,"")
chk("M13","5 cm class swath-to-swath max (0.16 ft)",0.26,1.6*5/30.48,0.005,"ft")
chk("M19","650,000 ft: US vs intl foot difference (ft)",1.30,650000*(1200/3937)/FT-650000,0.005,"ft")
chk("M19","1,200,000 US ft in m",365760.7315,1200000*1200/3937,0.0001,"m")
chk("M19","Difference 0.7315 m in ft",2.40,0.7315/FT,0.005,"ft")
with open("review/Technical_Review_Log.txt","w") as f:
    f.write("TECHNICAL REVIEW LOG - Mobile LiDAR Survey Seminar\nAutomated independent recomputation of key printed values (tech_review.py)\n")
    f.write("Generated October 2026. 'CHECK' means the printed value differs from the recomputed value beyond rounding.\n\n")
    f.write(f"{'Module':8}{'Item':58}{'Printed':>14}{'Recomputed':>16}  {'Unit':8}Result\n"+"-"*112+"\n")
    for m,i,p,cpt,u,r in rows: f.write(f"{m:8}{i:58}{p:>14}{cpt:>16}  {u:8}{r}\n")
    n=sum(r[5]=="PASS" for r in rows)
    f.write(f"\n{n} of {len(rows)} values PASS.\n")
    f.write("""
SCOPE AND LIMITS OF THIS REVIEW
- This is an arithmetic/consistency review: each value is recomputed from the stated inputs and
  from the manufacturer datasheets cited in each module's SOURCES box (Ouster OS0 Rev8, MicroStrain
  3DM-GX5-25/-45 and 3DM-GQ7, RIEGL VUX-240^24 dated 2026-08-17).
- Corrections made during review: Module 21 RMSE_H computation now shows the unrounded 2.634 cm;
  Try It 19.4 (U.S. vs international foot) corrected to 0.7315 m = 2.40 ft; ASPRS Table 7.2 limits
  (0.60X / 0.80X / 1.60X) verified against Edition 2, Version 2 (2024).
- Values still labeled 'typical' or 'read from chart' are intentionally so: OS0 precision versus
  range (read from the datasheet chart), ch.4 range-noise illustrations, and LiDAR reflectivity of
  materials (vary with wavelength, wetness and incidence angle).
- FDOT TML numeric tolerances (Handbook Sec. 39.6.2 / Appendix C) are left as a fill-in table; enter
  them from the current FDOT Surveying and Mapping Handbook.
- NOT DONE BY THE AUTHOR'S TOOLS: an independent review by a second Florida PSM. Module 19 contains a
  reviewer sign-off block that must be completed before the seminar is offered for CE credit.

Second PSM reviewer: ______________________  License No. ________  Date ___________
""")
print(open("review/Technical_Review_Log.txt").read()[-1800:])

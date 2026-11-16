import sys, glob, os, pandas as pd
root=sys.argv[1]; C=["car","motorbike","bus","truck"]; out=[]
for f in sorted(glob.glob(root+"/**/*.csv", recursive=True)):
    df=pd.read_csv(f).dropna(how="all"); cam=os.path.basename(os.path.dirname(f)); day=os.path.basename(f).split("_")[1]
    for d,g in df.groupby("Direction"):
        hrs=(pd.to_timedelta(g.Time).max()-pd.to_timedelta(g.Time).min()).total_seconds()/3600
        out.append(dict(cam=cam,day=day,dir=d,hrs=hrs,**{c:g[c].max() for c in C}))
o=pd.DataFrame(out); o["veh"]=o[C].sum(axis=1)
# per camera-day totals (merge main + _one) -> veh/hour
cd=o.groupby(["cam","day"]).agg(veh=("veh","sum"),hrs=("hrs","max")).reset_index()
cd["hrs"]=o.groupby(["cam","day","dir"]).hrs.sum().groupby(["cam","day"]).max().values
cd["vph"]=cd.veh/cd.hrs
print("veh/hour per camera across days (mean, CV%, min, max):")
g=cd.groupby("cam").vph; print(pd.DataFrame({"mean":g.mean().round(0),"cv%":(g.std()/g.mean()*100).round(0),"min":g.min().round(0),"max":g.max().round(0)}).to_string())
print("\ndirection share % per camera:")
print((o.groupby(["cam","dir"]).veh.sum().unstack()/o.groupby("cam").veh.sum().values[:,None]*100).round(0).to_string())
print("\nmotorbike share % per camera:", (o.groupby("cam").motorbike.sum()/o.groupby("cam").veh.sum()*100).round(0).to_dict())

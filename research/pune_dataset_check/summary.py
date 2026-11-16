import sys, glob, os, pandas as pd
root = sys.argv[1]; C=["car","motorbike","bus","truck"]; rows=[]
for f in sorted(glob.glob(root+"/**/*.csv", recursive=True)):
    df = pd.read_csv(f).dropna(how="all")
    if df.empty: rows.append(dict(file=os.path.basename(f), empty=True)); continue
    t = pd.to_timedelta(df.Time)
    resets = 0; tot = {c:0 for c in C}
    for d,g in df.groupby("Direction"):
        for c in C:
            v = g[c].to_numpy(); drops = (v[1:] < v[:-1]).sum(); resets += int(drops)
            tot[c] += int(v.max())  # ponytail: assumes no mid-file counter reset; 'resets' column flags it
    dur_h = (t.max()-t.min()).total_seconds()/3600
    tw = t.diff().dt.total_seconds()
    rows.append(dict(file=os.path.basename(f), cam=os.path.basename(os.path.dirname(f)), start=df.Time.iloc[0], end=df.Time.iloc[-1],
        hours=round(dur_h,2), gap_s_max=round(tw.max(),0), resets=resets, **tot, veh=sum(tot.values())))
s = pd.DataFrame(rows); pd.set_option("display.width",250); pd.set_option("display.max_rows",200)
print(s.to_string(index=False))
s.to_csv(sys.argv[2], index=False)
v = s.dropna(subset=["hours"]); v = v[v.hours>0]
print("\nTOTAL hours:", round(v.hours.sum(),1), " vehicles:", int(v.veh.sum()))
print("modal share %:", (v[C].sum()/v[C].sum().sum()*100).round(1).to_dict())
print("hours per camera:", v.groupby("cam").hours.sum().round(1).to_dict())
print("files with resets:", int((v.resets>0).sum()))

import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter
from pathlib import Path
import os

# ---------------------
# 1. Load the datasets
# ---------------------

# Update file paths if necessary
demographics_file = "data/demographics_data.csv"
spiro_file = "data/spirotidydatafinal.txt"
timezero_file = "data/Timezero File.xlsx"

# Read input files
demographics_df = pd.read_csv(demographics_file)
spiro_df = pd.read_csv(spiro_file)  # Use delimiter="\t" or delim_whitespace=True if needed
timezero_df = pd.read_excel(timezero_file)

# Standardize column names
spiro_df.rename(columns={"ID": "Id"}, inplace=True)
timezero_df.rename(columns={"New ID": "New_ID", "Time Zero": "Time_Zero"}, inplace=True)

# Merge with time-zero info
spiro_df = pd.merge(
    spiro_df,
    timezero_df,
    how="left",
    left_on=["Id", "Trial"],
    right_on=["New_ID", "Trial"]
)

# Drop extra merge columns
spiro_df.drop(columns=["New_ID"], inplace=True)

# Align time
spiro_df["Aligned_Time"] = spiro_df["Time"] - spiro_df["Time_Zero"]

# --- Function to calculate metrics ---
def compute_pft_metrics(df):
    df = df.dropna(subset=["Aligned_Time", "Volume", "Flow"])
    if df.empty or df["Aligned_Time"].max() < 6:
        return None

    # Sort
    df = df.sort_values("Aligned_Time")
    t = df["Aligned_Time"].values / 1000  # convert ms to seconds
    v = df["Volume"].values
    f = df["Flow"].values

    # Smooth volume if needed
    v_smooth = savgol_filter(v, window_length=11, polyorder=3)

    # Interpolate to get uniform time steps
    t_uniform = np.linspace(0, t[-1], num=500)
    v_interp = interp1d(t, v_smooth, bounds_error=False, fill_value="extrapolate")(t_uniform)
    f_interp = interp1d(t, f, bounds_error=False, fill_value="extrapolate")(t_uniform)

    # Compute FVC
    fvc = np.max(v_interp) - np.min(v_interp)

    # Compute FEV1 (volume at 1 second)
    fev1 = np.interp(1.0, t_uniform, v_interp)

    # Compute PEF (max flow)
    pef = np.max(f_interp)

    # Compute FEF25–75%
    v_start = np.min(v_interp)
    v_25 = v_start + 0.25 * fvc
    v_75 = v_start + 0.75 * fvc
    t_25 = np.interp(v_25, v_interp, t_uniform)
    t_75 = np.interp(v_75, v_interp, t_uniform)

    if t_75 > t_25:
        volumes_in_range = v_interp[(t_uniform >= t_25) & (t_uniform <= t_75)]
        times_in_range = t_uniform[(t_uniform >= t_25) & (t_uniform <= t_75)]
        fef25_75 = (volumes_in_range[-1] - volumes_in_range[0]) / (times_in_range[-1] - times_in_range[0])
    else:
        fef25_75 = np.nan

    return {
        "FEV1": round(fev1, 4),
        "FVC": round(fvc, 4),
        "PEF": round(pef, 4),
        "FEV1/FVC": round(fev1 / fvc, 6) if fvc > 0 else np.nan,
        "FEF25_75": round(fef25_75, 6)
    }

# --- Compute metrics for each trial ---
results = []

grouped = spiro_df.groupby(["Id", "Visit", "Trial"])
for (pid, visit, trial), group in grouped:
    metrics = compute_pft_metrics(group)
    if metrics:
        metrics.update({"Id": pid, "Visit": visit, "Trial": trial})
        results.append(metrics)

results_df = pd.DataFrame(results)

# --- Merge with demographics ---
final_df = results_df.merge(demographics_df, left_on="Id", right_on="ID", how="left")

# --- Export per-patient CSVs ---
output_dir = "patient_reports"
os.makedirs(output_dir, exist_ok=True)

for patient_id, group in final_df.groupby("Id"):
    filename = f"patient_{patient_id}.csv"
    filepath = os.path.join(output_dir, filename)
    group.to_csv(filepath, index=False)

print(f"✅ Exported {final_df['Id'].nunique()} patient reports to '{output_dir}/'")
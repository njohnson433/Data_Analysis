import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.patches as mpatches

# drops all the rows which have NA in them
def drop_NA(data):
    data_filtered = data.dropna().reset_index(drop=True)
    return data_filtered

# Load CSV file
data_robot = pd.read_csv(r'C:\Users\drnil\OneDrive - ETH Zurich\ETH\Msc\Data_Analysis\data\Drill_User_Study - Test Group.csv', encoding='ISO-8859-1',na_values=["NA","","#DIV/0!"])
data_manual = pd.read_csv(r'C:\Users\drnil\OneDrive - ETH Zurich\ETH\Msc\Data_Analysis\data\Drill_User_Study - Control Group.csv', encoding='ISO-8859-1',na_values=["NA","","#DIV/0!"])

sp_data = data_robot[['ID','SP1 [mm]','SP2 [mm]','SP3 [mm]']]
sp_data_manual = data_manual[['ID','SP1','SP2','SP3']]

# filter the data with the desired strategy
sp_data_filtered = drop_NA(sp_data)
sp_data_filtered_manual = drop_NA(sp_data_manual)

# get series per bone type for robotic assistance
robot_generic = sp_data_filtered['SP1 [mm]']
manual_generic = sp_data_filtered_manual['SP1']

robot_femur   = sp_data_filtered['SP2 [mm]']
manual_femur = sp_data_filtered_manual['SP2']

robot_ulna   = sp_data_filtered['SP3 [mm]']
manual_ulna = sp_data_filtered_manual['SP3']

snb_values_experienced = np.array([
        4.7, 2.7, 9.3, 6.0, 12.0, 5.3, 2.7, 3.3, 3.0, 3.0,
        5.3, 3.7, 7.7, 9.3, 0.7, 3.3, 8.7, 2.0, 7.7, 1.3
    ])

snb_values_inexperienced = np.array([
        14.0, 8.3, 4.0, 7.7, 8.0, 5.7, 3.0, 8.0, 9.0, 7.0, 
        9.7, 8.0, 17.7, 4.0, 7.7, 3.0, 5.0
    ])

# --- Organize data ---
data_robot = [robot_generic, robot_femur, robot_ulna]
data_manual = [manual_generic, manual_femur, manual_ulna]
bone_labels = ["Generic", "Femur", "Ulna"]
bone_colors = {"Generic": "red", "Femur": "green", "Ulna": "blue"}

# --- Positioning using np.arange ---
n_groups = len(data_robot)
barWidth = 0.35
br1 = np.arange(n_groups)
br2 = br1 + barWidth

fig, ax = plt.subplots(figsize=(8, 5), layout="constrained")

# --- Manual boxplots (with hatching) ---
bp_manual = ax.boxplot(
    data_manual,
    positions=br1,
    widths=0.3,
    patch_artist=True,
    showfliers=False
)

# --- Robot boxplots (no hatching) ---
bp_robot = ax.boxplot(
    data_robot,
    positions=br2,
    widths=0.3,
    patch_artist=True,
    showfliers=False
)

# --- Apply color + hatching per bone type ---
for patch, color in zip(bp_manual["boxes"], bone_colors.values()):
    patch.set_facecolor(color)
    patch.set_edgecolor("black")
    patch.set_linewidth(1.2)
    patch.set_hatch("//")  # hatching for manual group

for patch, color in zip(bp_robot["boxes"], bone_colors.values()):
    patch.set_facecolor(color)
    patch.set_edgecolor("black")
    patch.set_linewidth(1.2)

# --- Style whiskers, caps, medians ---
for k in ["whiskers", "caps", "medians"]:
    for line in bp_manual[k] + bp_robot[k]:
        line.set_color("black")
        line.set_linewidth(1.2)

# --- Labels & layout ---
ax.set_xticks(br1 + barWidth / 2)
ax.set_xticklabels(bone_labels)
ax.set_ylabel("Penetration Depth [mm]")
ax.set_title("Soft Tissue Penetration: Manual Control Laypeople vs Robotic Assistance Laypeople")
ax.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.6)

# --- Bone type legend (colors) ---
bone_handles = [
    mpatches.Patch(facecolor=color, edgecolor="black", label=bt)
    for bt, color in bone_colors.items()
]
bone_legend = ax.legend(handles=bone_handles, title="Bone Type", loc='upper left', ncols=3)
ax.add_artist(bone_legend)   # keep this legend when adding another

# --- Control type legend (hatching) ---
controller_handles = [
    mpatches.Patch(facecolor="white", edgecolor="black", hatch="//", label="Manual Control"),
    mpatches.Patch(facecolor="white", edgecolor="black", hatch="", label="Robotic Assistance")
]
ax.legend(handles=controller_handles, title="Control Type", loc='upper right')

plt.show()

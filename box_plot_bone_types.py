import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Load CSV file
data = pd.read_csv('Data/Drill_User_Study_Adapted_sheet.csv', encoding='ISO-8859-1')
# Get series per controller
manual = data.loc[data['Controller Activated']==0, 'Plunge-Depth [mm]'].dropna()

# get series per bone type for robotic assistance
robot_generic = data.loc[(data['Controller Activated']==1) & (data['Bone-Type']=='Generic'), 'Plunge-Depth [mm]'].dropna()
robot_tibia   = data.loc[(data['Controller Activated']==1) & (data['Bone-Type']=='Tibia'), 'Plunge-Depth [mm]'].dropna()
robot_femur   = data.loc[(data['Controller Activated']==1) & (data['Bone-Type']=='Femur'), 'Plunge-Depth [mm]'].dropna()

snb_values_experienced = np.array([
        4.7, 2.7, 9.3, 6.0, 12.0, 5.3, 2.7, 3.3, 3.0, 3.0,
        5.3, 3.7, 7.7, 9.3, 0.7, 3.3, 8.7, 2.0, 7.7, 1.3
    ])

snb_values_inexperienced = np.array([
        14.0, 8.3, 4.0, 7.7, 8.0, 5.7, 3.0, 8.0, 9.0, 7.0, 
        9.7, 8.0, 17.7, 4.0, 7.7, 3.0, 5.0
    ])

fig, ax = plt.subplots(layout="constrained", figsize=(6,4))

bp = ax.boxplot(
    [robot_generic, robot_femur, robot_tibia],
    labels=["Generic", "Femur", "Tibia"],
    patch_artist=True,          # allows coloring
    widths=0.6,
    showfliers=False,
)

# Colors + outlines
colors = ["blue", "red", "green"]
for patch, c in zip(bp["boxes"], colors):
    patch.set_facecolor(c)
    patch.set_edgecolor("black")
    patch.set_linewidth(1.2)

for k in ["whiskers", "caps", "medians"]:
    for line in bp[k]:
        line.set_color("black")
        line.set_linewidth(1.2)

ax.set_ylabel("Penetration Depth [mm]")
ax.set_title("Robotic Assistance Penetration Depth Comparison Bone Types")
ax.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.6)
#ax.legend([bp["boxes"][0], bp["boxes"][1], bp["boxes"][2],bp["boxes"][3]], ["Manual Control (MC)", "Robotic Assistance", "MC Experienced Surgeons", "MC Inexperienced Surgeon"], loc="upper right")

# Calculate median and standard deviation for each dataset
data_sets = [robot_generic, robot_femur, robot_tibia]

legend_labels = []
for dataset in data_sets:
    median_val = np.median(dataset)
    std_val = np.std(dataset)
    legend_labels.append(f"x̃: {median_val:.1f} mm, σ: {std_val:.1f} mm")

ax.legend([bp["boxes"][0], bp["boxes"][1], bp["boxes"][2]], 
          legend_labels, loc="upper right")


# print median and std for each bone type
print("Mean, Median and Standard Deviation for each bone type:")
for label, dataset in zip(["Generic", "Femur", "Tibia"], data_sets
    ):
    mean_val = np.mean(dataset)
    median_val = np.median(dataset)
    std_val = np.std(dataset)
    print(f"{label}: Mean = {mean_val:.2f} mm, Median = {median_val:.2f} mm, Standard Deviation = {std_val:.2f} mm")


#plt.show()

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# drops all the rows which have NA in them
def drop_NA(data):
    data_filtered = data.dropna().reset_index(drop=True)
    return data_filtered

# Load CSV file
data = pd.read_csv(r'C:\Users\drnil\OneDrive - ETH Zurich\ETH\Msc\Data_Analysis\data\Drill_User_Study - Test Group.csv', encoding='ISO-8859-1',na_values=["NA","","#DIV/0!"])

sp_data = data[['ID','SP1 [mm]','SP2 [mm]','SP3 [mm]']]

# filter the data with the desired strategy
sp_data_filtered = drop_NA(sp_data)

# get series per bone type for robotic assistance
robot_generic = sp_data_filtered['SP1 [mm]']
robot_femur   = sp_data_filtered['SP2 [mm]']
robot_ulna   = sp_data_filtered['SP3 [mm]']

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
    [robot_generic, snb_values_experienced, snb_values_inexperienced],
    labels=["Robotic Assisted Laypeople", "Experienced Surgeons", "Inexperienced Surgeons"],
    patch_artist=True,          # allows coloring
    widths=0.6,
    showfliers=False,
)

# Colors + outlines
colors = ["red", "orange", "purple"]
for patch, c in zip(bp["boxes"], colors):
    patch.set_facecolor(c)
    patch.set_edgecolor("black")
    patch.set_linewidth(1.2)

for k in ["whiskers", "caps", "medians"]:
    for line in bp[k]:
        line.set_color("black")
        line.set_linewidth(1.2)

ax.set_ylabel("Penetration Depth [mm]")
ax.set_title("Soft Tissue Penetration Normal Bone Group Comparison")
ax.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.6)
#ax.legend([bp["boxes"][0], bp["boxes"][1], bp["boxes"][2],bp["boxes"][3]], ["Manual Control (MC)", "Robotic Assistance", "MC Experienced Surgeons", "MC Inexperienced Surgeon"], loc="upper right")

# Calculate median and standard deviation for each dataset
data_sets = [robot_generic, snb_values_experienced, snb_values_inexperienced]

legend_labels = []
for dataset in data_sets:
    mean_val = np.mean(dataset)
    std_val = np.std(dataset)
    legend_labels.append(f"x̃: {mean_val:.1f} mm, σ: {std_val:.1f} mm")

ax.legend([bp["boxes"][0], bp["boxes"][1], bp["boxes"][2]], 
          legend_labels, loc="upper right")


# print median and std for each bone type
print("Mean, Median and Standard Deviation for each user group:")
for label, dataset in zip(["Robotic Assisted Laypeople", "Surgeons Experienced", "Surgeons Inexperienced"], data_sets
    ):
    mean_val = np.mean(dataset)
    median_val = np.median(dataset)
    std_val = np.std(dataset)
    print(f"{label}: Mean = {mean_val:.2f} mm, Median = {median_val:.2f} mm, Standard Deviation = {std_val:.2f} mm")


plt.show()

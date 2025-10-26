import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.patches as mpatches


# Load CSV file
data = pd.read_csv('Data/Drill_User_Study_Adapted_sheet.csv', encoding='ISO-8859-1')

data = data.sort_values('Participant')

participants = data['Participant'].unique()

# Create drill_data dictionary grouped by controller activation
drill_data = {}
bone_types = []  # one entry per participant

bone_colors = {"Generic": "blue", "Ulna": "green", "Femur": "orange"}

# Loop over controller values (0 = manual, 1 = robotic)
for controller_value in sorted(data['Controller Activated'].unique()):
    controller_data = data[data['Controller Activated'] == controller_value]

    plunge_depths = []
    for participant in participants:
        participant_data = controller_data[controller_data['Participant'] == participant]

        if not participant_data.empty:
            plunge_depths.append(participant_data['Plunge-Depth [mm]'].values[0])

            # only record Bone-Type once (first controller group)
            if controller_value == sorted(data['Controller Activated'].unique())[0]:
                bone_types.append(participant_data['Bone-Type'].values[0])
        else:
            plunge_depths.append(np.nan)  # use np.nan if missing

    label = 'Robotic Assistance' if controller_value == 1 else 'Manual Control'
    drill_data[label] = plunge_depths



# Set up bar plot
spacing = 5
x = np.arange(len(participants)) * spacing  # the label locations
width = 1.5  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(layout = "constrained")

for attribute, measurement in drill_data.items():
    offset = width * multiplier
    ls = None if attribute == 'Robotic Assistance' else '//'
    rects = ax.bar(x + offset, measurement, width, color=[bone_colors[bt] for bt in bone_types], edgecolor='black', linewidth=1, hatch=ls)
    ax.bar_label(rects, padding=3, fontsize=9)
    multiplier += 1


# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Penetration Depth [mm]')
ax.set_title('Soft Tissue Penetration Depth')
ax.set_xticks(x + width, participants)
ax.set_ylim(0, 30)

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


# show the plot
plt.show()


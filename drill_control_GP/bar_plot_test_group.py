import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.patches as mpatches

# drops all the rows which have NA in them
def drop_NA(data):
    data_filtered = data.dropna().reset_index(drop=True)
    return data_filtered


# Load CSV file
data = pd.read_csv(r'C:\Users\drnil\OneDrive - ETH Zurich\ETH\Msc\Data_Analysis\data\Drill_User_Study - Test Group.csv', encoding='ISO-8859-1',na_values=["NA","","#DIV/0!"])

data = data.sort_values('ID')

participants = data['ID'].unique()

sp_data = data[['ID','SP1 [mm]','SP2 [mm]','SP3 [mm]', 'SP_E1 [mm]', 'SP_E2 [mm]','SP_E3 [mm]']]

# filter the data with the desired strategy
data_filtered = drop_NA(sp_data)

abs_mean_error = data_filtered[['SP_E1 [mm]', 'SP_E2 [mm]','SP_E3 [mm]']].abs().mean().mean()


barWidth = 0.25
fig = plt.subplots(figsize =(12, 8)) 

br1 = np.arange(len(data_filtered['SP1 [mm]'])) 
br2 = [x + barWidth for x in br1] 
br3 = [x + barWidth for x in br2] 

plt.bar(br1, data_filtered['SP1 [mm]'], color ='r', width = barWidth, 
        edgecolor ='grey', label ='Generic') 
plt.bar(br2, data_filtered['SP2 [mm]'], color ='g', width = barWidth, 
        edgecolor ='grey', label ='Femur') 
plt.bar(br3, data_filtered['SP3 [mm]'], color ='b', width = barWidth, 
        edgecolor ='grey', label ='Ulna') 

plt.errorbar(br1, data_filtered['SP1 [mm]'], yerr=abs_mean_error, fmt="o",color="k")
plt.errorbar(br2, data_filtered['SP2 [mm]'], yerr=abs_mean_error, fmt="o",color="k")
plt.errorbar(br3, data_filtered['SP3 [mm]'], yerr=abs_mean_error, fmt="o",color="k")
plt.xlabel('Participant ID', fontsize = 15) 
plt.ylabel('Soft Tissue Penetration [mm]', fontsize = 15) 
plt.xticks([r + barWidth for r in range(len(data_filtered))], 
        data_filtered['ID'])
plt.legend()
plt.title('Soft Tissue Penertration Test Group')

# show the plot
plt.show()


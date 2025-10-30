from pdb import main
import numpy as np  
from scipy import stats
import matplotlib.pyplot as plt
import pandas as pd
import math


def one_sided_t_test(test_group,control_group):
# Population Mean 
    mu = control_group.mean()

    # Sample Size
    N1 = len(test_group)

    # Degrees of freedom  
    dof = N1 - 1

    # sample data
    x = robot

    # Using the Stats library, compute t-statistic and p-value
    t_stat, p_val = stats.ttest_1samp(a=x, popmean = mu)
    print("Null Hypothesis:" + str(mu))
    print("mean of sample data:", round(np.mean(x), 3))
    print("standard deviation of sample data:", round(np.std(x), 3))
    print("t-statistic = " + str(t_stat))  
    print("p-value = " + str(p_val))

    if p_val < 0.05:
        print("We reject the null hypothesis")
    else:
        print("We fail to reject the null hypothesis")

def welch_t_test(test_group, control_group):
    # Welch t-test: comparing robot group vs control group
    # Using equal_var=False for Welch t-test (assumes unequal variances)
    t_stat, p_val = stats.ttest_ind(test_group, control_group, equal_var=False)

    print("Welch t-test: Robot vs Control Group")
    print("Robot group - mean:", round(np.mean(test_group), 3), "std:", round(np.std(test_group), 3), "n:", len(test_group))
    print("Control group - mean:", round(np.mean(control_group), 3), "std:", round(np.std(control_group), 3), "n:", len(control_group))
    print("t-statistic =", round(t_stat, 4))
    print("p-value =", p_val)

    alpha = 0.05
    if p_val < alpha:
        print(f"We reject the null hypothesis (p < {alpha})")
        print("There is a significant difference between the two groups")
    else:
        print(f"We fail to reject the null hypothesis (p >= {alpha})")
        print("There is no significant difference between the two groups")

def effect_size(test_group, control_group):
    # calculate length of 1st sample
    n1 = len(control_group)

    # calculate length of 2nd sample
    n2 = len(test_group)

    SD1 = np.std(control_group)
    SD2 = np.std(test_group)

    mean_1 = np.mean(control_group)
    mean_2 = np.mean(test_group)

    pooled_standard_deviation = math.sqrt(
                        ((n1 - 1)*SD1 * SD1 +
                        (n2-1)*SD2 * SD2) / 
                                    (n1 + n2-2))
    
    e_size = (mean_1 - mean_2) / pooled_standard_deviation

    print("Effect Size =", e_size)
    

def std_from_mean(x, mean, sample):
    x = np.asarray(x)
    # sum of squared deviations
    ssd = np.sum((x - mean)**2)
    n = x.size
    if sample:
        return np.sqrt(ssd/(n-1))
    else:
        return np.sqrt(ssd/n)
    
    
# drops all the rows which have NA in them
def drop_NA(data):
    data_filtered = data.dropna().reset_index(drop=True)
    return data_filtered

    
# Load CSV file
data_robot = pd.read_csv(r'C:\Users\drnil\OneDrive - ETH Zurich\ETH\Msc\Data_Analysis\data\Drill_User_Study - Test Group.csv', encoding='ISO-8859-1',na_values=["NA","","#DIV/0!"])
data_manual = pd.read_csv(r'C:\Users\drnil\OneDrive - ETH Zurich\ETH\Msc\Data_Analysis\data\Drill_User_Study - Control Group.csv', encoding='ISO-8859-1',na_values=["NA","","#DIV/0!"])

data_robot_tlx = pd.read_csv(r'C:\Users\drnil\OneDrive - ETH Zurich\ETH\Msc\Data_Analysis\data\Drill_User_Study - Robot TLX Scores.csv', encoding='ISO-8859-1',na_values=["NA","","#DIV/0!"])
data_manual_tlx = pd.read_csv(r'C:\Users\drnil\OneDrive - ETH Zurich\ETH\Msc\Data_Analysis\data\Drill_User_Study - Manual TLX scores .csv', encoding='ISO-8859-1',na_values=["NA","","#DIV/0!"])

data_robot_tlx = data_robot_tlx[['Mental Demand','Physical Demand','Temporal Demand','Performance','Effort','Frustration']]
data_manual_tlx = data_manual_tlx[['Mental Demand','Physical Demand','Temporal Demand','Performance','Effort','Frustration']]


robot_tlx_mental = data_robot_tlx['Mental Demand']
manual_tlx_mental = data_manual_tlx['Mental Demand']

robot_tlx_phy = data_robot_tlx['Physical Demand']
manual_tlx_phy = data_manual_tlx['Physical Demand']

robot_tlx_temp = data_robot_tlx['Temporal Demand']
manual_tlx_temp = data_manual_tlx['Temporal Demand']

robot_tlx_per = data_robot_tlx['Performance']
manual_tlx_per = data_manual_tlx['Performance']

robot_tlx_eff = data_robot_tlx['Effort']
manual_tlx_eff = data_manual_tlx['Effort']

robot_tlx_frust = data_robot_tlx['Frustration']
manual_tlx_frust = data_manual_tlx['Frustration']

sp_data = data_robot[['ID','SP1 [mm]','SP2 [mm]','SP3 [mm]']]
sp_data_manual = data_manual[['ID','SP1 [mm]','SP2 [mm]','SP3 [mm]']]
sp_error_data = data_robot[['SP_E1 [mm]','SP_E2 [mm]','SP_E3 [mm]']]

# filter the data with the desired strategy
sp_data_filtered = drop_NA(sp_data)
sp_data_filtered_manual = drop_NA(sp_data_manual)
sp_error_data_filtered = drop_NA(sp_error_data)

robot_all = sp_data_filtered[['SP1 [mm]','SP2 [mm]','SP3 [mm]']]
manual_all = sp_data_filtered_manual[['SP1 [mm]','SP2 [mm]','SP3 [mm]']]

sp_error_data_filtered_all = sp_error_data_filtered.values.flatten()
robot_all    = robot_all.values.flatten()      # robot
manual_all = manual_all.values.flatten()     # manual/control

# get series per bone type for robotic assistance
robot_generic = sp_data_filtered['SP1 [mm]']
robot_generic_error = sp_error_data_filtered['SP_E1 [mm]']
manual_generic = sp_data_filtered_manual['SP1 [mm]']

robot_femur   = sp_data_filtered['SP2 [mm]']
robot_femur_error = sp_error_data_filtered['SP_E2 [mm]']
manual_femur = sp_data_filtered_manual['SP2 [mm]']

robot_ulna   = sp_data_filtered['SP3 [mm]']
robot_ulna_error = sp_error_data_filtered['SP_E3 [mm]']
manual_ulna = sp_data_filtered_manual['SP3 [mm]']

robot_generic_error_std = std_from_mean(sp_error_data_filtered_all,0,sample=True)

print("std of errors in sp measurement to zero", robot_generic_error_std)

snb_values_experienced = np.array([
        4.7, 2.7, 9.3, 6.0, 12.0, 5.3, 2.7, 3.3, 3.0, 3.0,
        5.3, 3.7, 7.7, 9.3, 0.7, 3.3, 8.7, 2.0, 7.7, 1.3
    ])

snb_values_experienced_minus = snb_values_experienced - robot_generic_error_std

snb_values_inexperienced = np.array([
        14.0, 8.3, 4.0, 7.7, 8.0, 5.7, 3.0, 8.0, 9.0, 7.0, 
        9.7, 8.0, 17.7, 4.0, 7.7, 3.0, 5.0
    ])

### define which test to run ###
test = "welch"  # options: "one-sided", "welch"

if test == "one-sided":
    one_sided_t_test(robot_generic, snb_values_experienced)
elif test == "welch":
    welch_t_test(robot_all, manual_all)
else:
    print("Invalid test type. Please choose 'one-sided' or 'welch'.")


### calculate effect size (coehn's d)
effect_size(robot_generic, snb_values_experienced)

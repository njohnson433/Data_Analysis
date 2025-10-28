from pdb import main
import numpy as np  
from scipy import stats
import matplotlib.pyplot as plt
import pandas as pd  


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
    print("p-value =", round(p_val, 4))

    alpha = 0.05
    if p_val < alpha:
        print(f"We reject the null hypothesis (p < {alpha})")
        print("There is a significant difference between the two groups")
    else:
        print(f"We fail to reject the null hypothesis (p >= {alpha})")
        print("There is no significant difference between the two groups")

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

### define which test to run ###
test = "welch"  # options: "one-sided", "welch"

if test == "one-sided":
    one_sided_t_test(robot_generic, snb_values_experienced)
elif test == "welch":
    welch_t_test(robot_generic, snb_values_experienced)
else:
    print("Invalid test type. Please choose 'one-sided' or 'welch'.")
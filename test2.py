import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

from csv import DictReader

list_of_traces = []
raw_speed = []
# with open('data/address2.csv', 'r') as read_obj:
#     dicts = DictReader(read_obj)
#     list_of_traces = list_of_traces + list(dicts)
    
with open('data/address3.csv', 'r') as read_obj:
    dicts = DictReader(read_obj)
    list_of_traces = list_of_traces + list(dicts)

with open('data/address.csv', 'r') as read_obj:
    dicts = DictReader(read_obj)
    list_of_traces = list_of_traces + list(dicts)
    
for trace in list_of_traces:
   if float(trace['vehicle_speed']) > 5:
    raw_speed.append(float(trace['vehicle_speed']))
  

# Define input speed universe
speed = np.array(raw_speed)
# print(raw_speed)

# Define fuzzy membership functions for speed
low_speed = fuzz.trimf(speed, [0, 0, 50])
med_speed = fuzz.trimf(speed, [0, 50, 100])
high_speed = fuzz.trimf(speed, [50, 100, 100])

# Define fuzzy membership functions for output speed
low_out_speed = fuzz.trimf(speed, [0, 0, 50])
med_out_speed = fuzz.trimf(speed, [0, 50, 100])
high_out_speed = fuzz.trimf(speed, [50, 100, 100])

# Set input value
input_speed = 50

# Compute membership degrees for the input speed
low_speed_degree = fuzz.interp_membership(speed, low_speed, input_speed)
med_speed_degree = fuzz.interp_membership(speed, med_speed, input_speed)
high_speed_degree = fuzz.interp_membership(speed, high_speed, input_speed)

# Combine membership degrees using np.fmin to get output speed
output_speed = np.fmax(np.fmin(med_speed_degree, med_out_speed),
                       np.fmax(np.fmin(low_speed_degree, low_out_speed),
                               np.fmin(high_speed_degree, high_out_speed)))

print(low_speed)

# Defuzzify output speed to get a crisp value
crisp_speed = fuzz.defuzz(speed, output_speed, 'centroid')

# Plot membership degrees for input speed and output speed
fig, ax = plt.subplots()
ax.plot(speed, low_speed, 'b', linewidth=1.5, label='Low Speed')
ax.plot(speed, med_speed, 'g', linewidth=1.5, label='Medium Speed')
ax.plot(speed, high_speed, 'r', linewidth=1.5, label='High Speed')
ax.fill_between(speed, 0, output_speed, alpha=0.2)
ax.plot([crisp_speed, crisp_speed], [0, fuzz.interp_membership(speed, output_speed, crisp_speed)], 'k', linewidth=1.5, alpha=0.9)
ax.set_title('Input and Output Membership Functions')
ax.legend()

# Show plot
# plt.show()

# Print estimated output speed
print(f"Estimated output speed: {crisp_speed}")

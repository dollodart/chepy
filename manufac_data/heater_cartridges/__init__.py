import pandas as pd
df = pd.read_csv('heater-cartridges.csv', delimiter='|')
df = df.drop(columns=['Sheath Material', 'Max temp (F)']) # all inconel with max 1400 deg. F
df['Area (in^2)'] = 3.14159 * (df['Element Diameter (in)'] / 4.)**2 
df['Volume (in^3)'] = df['Element Length (in)'] * df['Area (in^2)']
df['Length/Area (1/in)'] = df['Element Length (in)'] / df['Area (in^2)']
df['Area/Length (in)'] = 1 / df['Length/Area (1/in)']
df['Volumetric Heat Rate (W/in^3)'] = df['Power (W)'] / df['Volume (in^3)']
df['Current Density (A/in^2)'] = df['Current at 120 VAC single phase (A)'] / df['Area (in^2)']
df['Heat Flux (W/in^2)'] = df['Power (W)'] / df['Area (in^2)'] # effectively power density
df['Linear Power Density (W/in)'] = df['Power (W)'] / df['Element Length (in)']

# current is directly related to power
# area, volume, length/area, and area/length are calculated from the given data
# though they may differ in linear correlation as a result of non-linear operations
ind_vars = ['Element Length (in)', 'Element Diameter (in)', 'Power (W)', 'Wire Lead Length (in)']
ind_vars.extend(['Area (in^2)', 'Volume (in^3)', 'Area/Length (in)']) # not independent, but expected different correlations
sdf = df[ind_vars]

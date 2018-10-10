#capstone project

#import codecademylib
import pandas as pd 
from matplotlib import pyplot as plt 
from scipy.stats import chi2_contingency
import math

#read csv into the data frame called 'species'
species = pd.read_csv('species_info.csv')
#print the first 5 lines of the species dataframe
print (species.head())

observations = pd.read_csv('observations.csv')
print (observations.head())

#creates a new column with the value True if the word Sheep is in the name (if it is a sheep) and False otherwise
species['is_sheep'] = species.common_names.apply(lambda x: 'Sheep' in x)
#create a dataframe of only those species that had True in the 'is_sheep' column
species_is_sheep = species[species.is_sheep]
#tightening the criteria to only include sheep that are also mammals
sheep_species = species[(species.is_sheep) & (species.category == 'Mammal')]
print (sheep_species)
sheep_observations = observations.merge(sheep_species)
print (sheep_observations.head())
#grouping the sheep_observations data by the park_name and including the sum of the observations at each location
obs_by_park = sheep_observations.groupby('park_name').observations.sum().reset_index()
print (obs_by_park)

#creating a bar chart showing the number of sheep sightings per week in each park
plt.figure(figsize = (16, 4))
ax = plt.subplot()
plt.bar(range(len(obs_by_park)), obs_by_park.observations)
ax.set_xticks(range(len(obs_by_park)))
ax.set_xticklabels(obs_by_park.park_name)
plt.ylabel('Number of Observations')
plt.title('Observations of Sheep per Week')
plt.show()

#fill in the empty slots in species that are currently Null with a value/argument of our choice
species.fillna('No Intervention', inplace = True)
#creates a new column which is True if the conservation_status is not equal to 'No Intervention' and False otherwise
species['is_protected'] = species.conservation_status != 'No Intervention'
#counts the number of unique scientific names in the species df
species_count = species.scientific_name.nunique()
#creates a list of unique categories in the species df
species_type = species.category.unique()
#creates a list of unique conservation statuses in the species df
conservation_statuses = species.conservation_status.unique()


#creates a df that uses the species df, groups it by 'conservation_status', and counts the number of unique species in each conservation status
conservation_counts_fixed = species.groupby('conservation_status').scientific_name.nunique().reset_index()
print (conservation_counts_fixed)
#section uses a pivot table to display which species categories are protected and which are not
#groups by 2 columns and the values are the number of unique scientific names in each
category_counts = species.groupby(['category', 'is_protected']).scientific_name.nunique().reset_index()
print (category_counts.head())
category_pivot = category_counts.pivot(columns = 'is_protected', \
									   index = 'category', \
									   values = 'scientific_name').reset_index()
print (category_pivot)
#renaming the columns in my pivot table
category_pivot.columns = ['category', 'not_protected', 'protected']
#creating a new column in the pivot table that shows the percentage of species that are protected
category_pivot['percent_protected'] = category_pivot.protected / (category_pivot.protected + category_pivot.not_protected)
print (category_pivot)


#plotting a bar graph with the values from the protection_counts df
protection_counts = species.groupby('conservation_status').scientific_name.nunique().reset_index().sort_values(by = 'scientific_name')

plt.figure(figsize = (10, 4))
ax = plt.subplot()
#plt.bar takes 2 arguments: (the number of bars being plotted- x) and (the heights of the x-values being plotted)
plt.bar(range(len(protection_counts)), protection_counts.scientific_name.values)
ax.set_xticks(range(len(protection_counts)))
ax.set_xticklabels(protection_counts.conservation_status.values)
plt.ylabel('Number of Species')
plt.title('Conservation Status by Species')
labels = [e.get_text() for e in ax.get_xticklabels()]
plt.show()

contingency = [[30, 146], \
			   [75, 413]]
contingency_2 = [[5, 73], \
				 [30, 146]]
chi_stat, pval, dof, expfrq = chi2_contingency (contingency)
chi_stat_2, pval_reptile_mammal, dof_2, expfrq_2 = chi2_contingency(contingency_2)
print (pval)
print (pval_reptile_mammal)

baseliine = 15
minimum_detectable_effect = 100 * 5 / 15
#according to a sample size calculator with a statistical significance of 90%
#note that the codecademy system didn't like this answer and required I use 510 to mark it right. 890 is accurate, though.
sample_size_per_variant = 890
#to determine how many weeks of observations are required at each park based on historical data to get to the designated sample size
#math.ceil returns the smallest integer greater than or equal to the number passed as an argument. 
yellowstone_weeks_observing = math.ceil(sample_size_per_variant / 507.0)
bryce_weeks_observing = math.ceil(sample_size_per_variant / 250.0)
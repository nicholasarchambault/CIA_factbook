#!/usr/bin/env python
# coding: utf-8

# # Analyzing CIA Factbook Data with SQL
# by Nicholas Archambault
# 
# In this project, we'll analyze data from the CIA Factbook, a compendium of statistics about every country on Earth. The Factbook includes the following demographic information:
# 
#    * `name` - The country's name
#    * `area` - Total land and sea area (square kilometers)
#    * `area_land` - Total land area (square kilometers)
#    * `area_water` - Total sea area (square kilometers)
#    * `population` - 2015 population
#    * `population_growth` - Population growth as a percentage
#    * `birth_rate` - Number of births per year per 1,000 people
#    * `death_rate` - Number of deaths per year per 1,000 people
#    * `migration_rate` - Number of emigrants per year per 1,000 people

# ## SQL Installation

# In[1]:


# !conda install -yc conda-forge ipython-sql


# In[2]:


get_ipython().run_cell_magic('capture', '', '%load_ext sql\n%sql sqlite:///factbook.db')


# In[3]:


get_ipython().run_cell_magic('sql', '', "SELECT *\n  FROM sqlite_master\n WHERE type='table';")


# ## Data Overview
# 
# Preview the data and select population statistics.

# In[4]:


get_ipython().run_cell_magic('sql', '', 'SELECT *\n  FROM facts\n LIMIT 5;')


# In[5]:


get_ipython().run_cell_magic('sql', '', 'SELECT MIN(population) AS min_pop, \n       MAX(population) AS max_pop, \n       MIN(population_growth) AS min_growth, \n       MAX(population_growth) AS max_growth\n  FROM facts;')


# The above summary statistics are noteworthy because they reveal that there are listed countries with populations of 0 and over 7.2 billion. We can zoom in on these entries with a subquery.

# In[6]:


get_ipython().run_cell_magic('sql', '', 'SELECT *\n  FROM facts\n WHERE population == (SELECT MIN(population)\n                        FROM facts);')


# In[7]:


get_ipython().run_cell_magic('sql', '', 'SELECT *\n  FROM facts\n WHERE population == (SELECT MAX(population)\n                        FROM facts);')


# As suspected, the two outlying data points are Antarctica and the entire World. Antarctica has an official population of 0, but it is a singular locale frequented by researchers and some visitors. As such, we won't eliminate it from the dataset.
# 
# The World, on the other hand, accounts for the populations of all countries on the planet. It is not a singular place, and its presence in the data would unduly distort calculations of averages and other statistics. For these reasons, we will eliminate it from the data.
# 
# We can recalculate the summary statistics from a dataset that does not include World.

# In[8]:


get_ipython().run_cell_magic('sql', '', 'SELECT MIN(population) AS min_pop, \n       MAX(population) AS max_pop, \n       MIN(population_growth) AS min_growth, \n       MAX(population_growth) AS max_growth\n  FROM facts\n WHERE name != "World";')


# The country with the highest population in the world approaches 1.4 billion people.

# ## Exploring Average Population and Area
# 
# We can explore density of inhabitation by examining the values of the population and area variables. Below, we look at the averages.

# In[9]:


get_ipython().run_cell_magic('sql', '', 'SELECT AVG(population) AS avg_pop, \n       AVG(area) AS avg_area\n  FROM facts\n WHERE name != "World";')


# The average population is 32.2 million people, while the average area is 555,000 square kilometers.

# ## Identifying Densely Populated Nations
# 
# Building off examination of these variables, we can identify densely populated countries. We determine that countries with this characterization are those with above average values for population and below average values for total area.

# In[10]:


get_ipython().run_cell_magic('sql', '', 'SELECT *\n  FROM facts\n WHERE population > (SELECT AVG(population)\n                       FROM facts)\n        AND area < (SELECT AVG(area)\n                      FROM facts);')


# Our final list of densely populated countries contains just seven nations, a result that may be surprising given the total number of countries in the world. We could further explore this characterization by introducing a more specific definition of 'densely populated' and investigating other factors -- some which may be unavailable in the Factbook itself -- that both contribute to and result from a nation's population density.

# ## Conclusion
# 
# In this project, we utilized basic features and techniques of SQL to explore the CIA Factbook and determine that only seven nations meet our rough definition of 'densely populated'.

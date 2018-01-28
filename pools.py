
# coding: utf-8

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
import math
import pandas as pd
from pandas.plotting import table
import matplotlib
matplotlib.style.use('seaborn-darkgrid')
import matplotlib.pyplot as plt
from IPython.display import display, Markdown, HTML, Javascript
from ipywidgets import widgets
from utils import human_size, selectdata, nextall, getrawdata, ExplorersSelection
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"


# In[ ]:


explorers=selectdata("/tmp/datazfssa")
f = ExplorersSelection('pools.csv', explorers)
f.widget()
continueall = widgets.Button(description="Continue", button_style='success')
continueall.on_click(nextall)
display(continueall)


# In[ ]:


InteractiveShell.ast_node_interactivity = "last_expr"


# In[ ]:


POOLSFILES = f.selected_explorers
POOLSFILES


# In[ ]:


dataraw = getrawdata(POOLSFILES)


# # Show available columns

# In[ ]:


dataraw.columns


# In[ ]:


# drop rows where the status is exported to avoid some duplicated values 
dataraw = dataraw[dataraw.status != 'exported']
countpools = dataraw[['asn']]
display(Markdown("### Pools: {}".format(len(countpools))))


# check profiles

# In[ ]:


profiles = dataraw[['profile', 'name', 'owner', 'status']].set_index('name').sort_index(ascending=True)
profiles


# check if more than one profile is in the same node

# In[ ]:


uniqref = profiles[profiles['status'] != 'exported']
uniq = uniqref.groupby('name')['profile']
if uniq.all().nunique() != len(uniqref):
    display(HTML('<strong><span style="background-color: #FFFF00">'
                 'Some pools with the same profile are in the same controller (Not Recommended).'
                 '</span></strong>'))
else:
    display(HTML('<strong>Pools per profile distributed normally</strong>'))
uniq.all()


# ### Get usage distribution
# 
# legend:
# 
#     usage_total = total pool capacity
#     usage_usage_total = total space used
#     usage_usage_data = space used (not considering reservation)
#     usage_used = real space used
#     usage_available = space available - reservation, etc
#     usage_free = space free for assigment
#     usage_usage_snapshots = space used for snapshots

# In[ ]:


poolsimported = dataraw.set_index('name')
poolsimported = poolsimported[profiles['status'] != 'exported']
usage = poolsimported[['usage_available', 'usage_used', 'usage_usage_data', 'usage_free',
                       'usage_usage_snapshots', 'usage_usage_total', 'usage_total']]
usage = usage.astype(float)
plt.figure(figsize=(30, 8))
# plot bar
ax1 = plt.subplot(121)
ax1 = usage.sort_index(ascending=True).astype(float).plot(kind='bar', legend=True, ax=ax1, fontsize=12, grid=True)
ax1.set_ylabel('Space Usage')
ax1.set_xlabel('pool')
plt.show()
usage.sort_index(ascending=True).applymap(human_size)


# In[ ]:


usagefree = usage[['usage_free', 'usage_total']]
usagefreepercent = (usagefree['usage_free'] * 100 ) / usagefree['usage_total']
usagefreepercent.rename("Usage Free Percentage", inplace=True).sort_index(ascending=True, inplace=True)
colors = []
for val in usagefreepercent:
    if val > 20:
        colors.append('g')
    elif val <= 20 and val > 10:
        colors.append('y')
    else:
        colors.append('r')
        
plt.figure(figsize=(16, 6))
# plot bar
ax1 = plt.subplot(121)
ax1 = usagefreepercent.astype(float).plot(kind='bar', ax=ax1, fontsize=12, grid=True, color=colors)
ax1.set_ylabel('Free Percent')
ax1.set_xlabel('pool')
# plot table
ax2 = plt.subplot(122)
plt.axis('off')
tbl = table(ax2, usagefreepercent.round(2), loc='center', bbox=[0.2, 0.2, 0.5, 0.5])
tbl.auto_set_font_size(False)
plt.show()


# ### Get compression info

# In[ ]:


compress = dataraw[['name', 'usage_compression']]
compress.set_index('name').sort_index(ascending=True)


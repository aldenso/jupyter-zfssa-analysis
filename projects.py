
# coding: utf-8

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
from pandas.plotting import table
import matplotlib
matplotlib.style.use('seaborn-darkgrid')
import matplotlib.pyplot as plt
from IPython.display import display, Markdown, HTML
from ipywidgets import widgets
from utils import human_size, selectdata, nextall, getrawdata, ExplorersSelection
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"


# In[ ]:


explorers=selectdata("/tmp/datazfssa")
f = ExplorersSelection('projects.csv', explorers)
f.widget()
continueall = widgets.Button(description="Continue", button_style='success')
continueall.on_click(nextall)
display(continueall)


# In[ ]:


InteractiveShell.ast_node_interactivity = "last_expr"


# In[ ]:


PROJFILES = f.selected_explorers
PROJFILES


# In[ ]:


dataraw = getrawdata(PROJFILES)


# Show available columns

# In[ ]:


dataraw.columns


# In[ ]:


countproj = dataraw['id'].count()
display(Markdown("### Projects count: {}".format(countproj)))


# ### Get projects per pool

# In[ ]:


projpool = dataraw[['name', 'pool']].rename(columns={'name': 'projects'}).groupby('pool').count()

plt.figure(figsize=(14, 9))
# plot bar
ax1 = plt.subplot(221)
ax1 = projpool.plot(kind='bar', legend=False, ax=ax1, fontsize=12, grid=True)
ax1.set_ylabel('Projects')
ax1.set_xlabel('pool')
# plot pie
ax3 = plt.subplot(222)
ax3 = projpool.plot(kind='pie', legend=False, ax=ax3, subplots=True, startangle=90)
# plot table
ax2 = plt.subplot(223)
plt.axis('off')
tbl = table(ax2, projpool, loc='center', bbox=[0.2, 0.2, 0.5, 0.5])
tbl.auto_set_font_size(False)
tbl.set_fontsize(14)
plt.show()


# ### Check for duplicated projects in different pools

# In[ ]:


projpool = dataraw[['name', 'pool']]
nonunique = projpool[projpool['name'].duplicated()].groupby('name')
dup = projpool[projpool.name.isin(nonunique.name.all())]
dup.set_index('name').sort_values('pool')


# ### Usage

# In[ ]:


sumspace = dataraw[['space_total', 'space_data','space_unused_res', 'space_unused_res_shares',
                    'reservation']].sum()
sumspace.map(human_size)


# ### Usage per pool

# In[ ]:


spacepool = dataraw[['space_total', 'space_data','space_unused_res', 'space_unused_res_shares',
                     'reservation', 'pool']].groupby('pool')
spacepool.sum().applymap(human_size)


# ### Get projects using compression

# In[ ]:


compress = dataraw[['name', 'pool', 'compressratio']]
compress[compress['compressratio'] != 100]


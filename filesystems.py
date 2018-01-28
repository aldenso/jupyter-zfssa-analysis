
# coding: utf-8

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
from pandas.plotting import table
import matplotlib
matplotlib.style.use('seaborn-darkgrid')
import matplotlib.pyplot as plt
from IPython.display import display, Markdown, HTML, Javascript
from IPython.core.interactiveshell import InteractiveShell
from ipywidgets import widgets
from utils import human_size, selectdata, nextall, getrawdata, ExplorersSelection
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"


# In[ ]:


explorers=selectdata("/tmp/datazfssa")
f = ExplorersSelection('filesystems.csv', explorers)
f.widget()
continueall = widgets.Button(description="Continue", button_style='success')
continueall.on_click(nextall)
display(continueall)


# In[ ]:


InteractiveShell.ast_node_interactivity = "last_expr"


# In[ ]:


FSFILES = f.selected_explorers
FSFILES


# In[ ]:


dataraw = getrawdata(FSFILES)


# Show available columns

# In[ ]:


dataraw.columns


# In[ ]:


countfs = dataraw['id'].count()
display(Markdown("#### FileSystems Count: {}".format(countfs)))


# ### Get Filesystems per pool

# In[ ]:


countfspool = dataraw[['id', 'pool']].rename(columns={'id': 'Filesystems'}).groupby('pool').count()

plt.figure(figsize=(16, 9))
# plot bar
ax1 = plt.subplot(221)
ax1 = countfspool.plot(kind='bar', legend=False, ax=ax1, fontsize=12, grid=True)
ax1.set_ylabel('FS Count')
ax1.set_xlabel('pool')
# plot table
ax2 = plt.subplot(222)
plt.axis('off')
tbl = table(ax2, countfspool, loc='center', bbox=[0.2, 0.2, 0.5, 0.5])
tbl.auto_set_font_size(False)
tbl.set_fontsize(14)
# plot pie
ax3 = plt.subplot(223)
ax3 = countfspool.plot(kind='pie', legend=False, subplots=True, ax=ax3, startangle=90)
plt.show()


# ### Usage

# In[ ]:


sumspace = dataraw[['space_total', 'space_data']].sum()
sumspace.map(human_size)


# In[ ]:


spacepool = dataraw[['space_total', 'space_data', 'pool']].groupby('pool')
spacepool.sum().applymap(human_size)


# ### Graphical comparison between space total usage and space data usage

# In[ ]:


plt.figure(figsize=(16, 4))
# plot bar
ax = plt.subplot(111)
ax = spacepool.sum().plot(kind='barh', legend=True, ax=ax, fontsize=12, grid=True)
ax.set_xlabel("Space (GB)")
plt.show()


# ### Get reservations
# 
# Get total reservations assigned and reservations per pool.

# In[ ]:


sumrestotal = dataraw[['reservation']].sum()
display(Markdown("#### Reservation total SUM: {}".format(human_size(sumrestotal.reservation))))


# In[ ]:


reservationpool = dataraw[['reservation', 'pool']].groupby('pool')
reservationpool.sum().applymap(human_size)


# In[ ]:


unusedrespool = dataraw[['space_unused_res', 'pool']].groupby('pool')
unusedrespool.sum().applymap(human_size)


# ### Show percentaje of unused reservation per filesystem in GB
# 
# Table with top unused reservation and a graph with red bars in values equal or beyond 50% percent.

# In[ ]:


InteractiveShell.ast_node_interactivity = "all"


# In[ ]:


def highlight(data):
    if data.space_unused_res > 50:
        return 'background-color: yellow'

unusedresfs = dataraw[['name', 'project', 'space_unused_res', 'reservation']]
percentage = unusedresfs.copy()
percentage['unused_percent'] = (unusedresfs['space_unused_res'] / unusedresfs['reservation']) * 100
percentage['used_percent'] = 100 - (unusedresfs['space_unused_res'] / unusedresfs['reservation']) * 100
percentage['space_unused_res'] = percentage['space_unused_res']
percentage['reservation'] = percentage['reservation']
percentage['space_unused_res'] = percentage['space_unused_res'].apply(human_size)
percentage['reservation'] = percentage['reservation'].apply(human_size)
percentage.set_index(['name', 'project'], inplace=True)
topunusedpercent = percentage.sort_values('unused_percent', ascending=False).dropna()
if topunusedpercent.empty:
    display(Markdown("### No unused reservation to report"))
else:
    topunusedpercent.style.bar()


# In[ ]:


InteractiveShell.ast_node_interactivity = "last_expr"


# In[ ]:


if not topunusedpercent.empty:
    colors = []
    for val in topunusedpercent['unused_percent'].values:
        if val >= 50:
            colors.append('r')
        else:
            colors.append('b')

    def vertical_size(count):
        if count <= 15:
            return 10
        else:
            size = (count / 15) * 5
            if size <= 10:
                return 10
            else:
                return ((count / 15) * 5)
    vertical = vertical_size(topunusedpercent.count()[0])
    plt.figure(figsize=(16, vertical))
    # plot bar
    ax = plt.subplot(111)
    ax = topunusedpercent['unused_percent'].plot(kind='barh', legend=False, ax=ax,
                                          fontsize=12, grid=True, stacked=True, color=colors)
    ax.set_ylabel('Unused Percentage')
    ax.set_xlabel('filesystem')
    plt.show()


# ### Get quota information

# In[ ]:


InteractiveShell.ast_node_interactivity = "all"


# In[ ]:


quotaref = dataraw[['project', 'name', 'quota', 'space_data']]
quota = quotaref.copy()
# leave just row with non-zero quota values
quota = quota[~(quota == 0).any(axis=1)]
quota['unused_percent'] = 100 - (quota['space_data'] / quota['quota']) * 100
quota['used percent'] = (quota['space_data'] / quota['quota']) * 100
quota['quota'] = quota['quota'].apply(human_size) #/ (1024 * 1024 * 1024)
quota['space_data'] = quota['space_data'].apply(human_size)
#quota.set_index('name', inplace=True)
quota.set_index(['name', 'project'], inplace=True)
topquotaunused = quota.sort_values('unused_percent', ascending=False)
if topquotaunused.empty:
    display(Markdown("### No unused quota to report"))
else:
    topquotaunused.style.bar()


# In[ ]:


InteractiveShell.ast_node_interactivity = "last_expr"


# In[ ]:


if not topquotaunused.empty:
    colors = []
    for val in topquotaunused['unused_percent'].values:
        if val >= 50:
            colors.append('r')
        else:
            colors.append('b')
    def vertical_size(count):
        if count <= 15:
            return 10
        else:
            size = (count / 15) * 5
            if size <= 10:
                return 10
            else:
                return ((count / 15) * 5)
    vertical = vertical_size(topquotaunused.count()[0])
    plt.figure(figsize=(16, vertical))
    # plot bar
    ax = plt.subplot(111)
    ax = topquotaunused['unused_percent'].plot(kind='barh', legend=False, ax=ax,
                                               fontsize=12, grid=True, stacked=True, color=colors)
    ax.set_ylabel('Unused Quota Percentage')
    ax.set_xlabel('filesystem')
    plt.show()


# ### Get filesystems using compression

# In[ ]:


compress = dataraw[['name', 'project', 'pool', 'compressratio']]
compress = compress[compress['compressratio'] != 100]
compress.set_index('name')


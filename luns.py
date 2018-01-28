
# coding: utf-8

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
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
f = ExplorersSelection('luns.csv', explorers)
f.widget()
continueall = widgets.Button(description="Continue", button_style='success')
continueall.on_click(nextall)
display(continueall)


# In[ ]:


InteractiveShell.ast_node_interactivity = "last_expr"


# In[ ]:


LUNSFILES = f.selected_explorers
LUNSFILES


# In[ ]:


dataraw = getrawdata(LUNSFILES)


# Show available columns

# In[ ]:


dataraw.columns


# ### Select only name, project, pool, volsize, lunumber, lunguid and space total cols

# In[ ]:


mydata = dataraw[['name', 'project', 'pool', 'volsize', 'lunumber', 'lunguid', 'space_total']]


# ### Get Total luns

# In[ ]:


display(Markdown("### Total luns: {}".format(mydata.count()[0])))


# ### Get luns per project

# In[ ]:


grpprojprool = mydata.groupby(['project', 'pool'])
grpprojprool.count()[['name']].rename(columns={'name': 'luns'}).sort_values('luns', ascending=False)


# ### Get all projects and all projects names with luns (including repeated in different pools)

# In[ ]:


projectslist = mydata.project.unique()
countproj, countprojperpool = len(projectslist), len(grpprojprool.indices)
display(Markdown("### Total project names with luns: {}\n\n ### Total projects with luns: {}"
                 .format(countproj, countprojperpool)))
if countproj != countprojperpool:
    display(HTML('<strong><span style="background-color: #FFFF00">'
                 'Some project names are repeated in different pools.'
                 '</span></strong>'))


# ### Get luns per pool

# In[ ]:


lunsperpool = mydata.groupby('pool').count()[['name']].rename(columns={'name': 'luns'})

plt.figure(figsize=(15, 9))
# plot bar
ax1 = plt.subplot(221)
ax1 = lunsperpool.plot(kind='barh', legend=False, ax=ax1, fontsize=12, grid=True)
ax1.set_ylabel('pool')
ax1.set_xlabel('luns')
# plot pie
ax2 = plt.subplot(222)
ax2 = lunsperpool.plot(kind='pie', legend=False, ax=ax2, subplots=True, startangle=90)
# plot table
ax3 = plt.subplot(223)
plt.axis('off')
tbl = table(ax3, lunsperpool, loc='center', bbox=[0.2, 0.2, 0.5, 0.5])
tbl.auto_set_font_size(False)
tbl.set_fontsize(14)
plt.show()


# ### Get usage size per pool
# 
# Shows graphs for volsize sum per pool and for space_total sum per pool.

# In[ ]:


volsperpool = grpprojprool['volsize'].sum().groupby('pool').sum() / (1024 * 1024 * 1024 * 1024)
spacetperpool = grpprojprool['space_total'].sum().groupby('pool').sum() / (1024 * 1024 * 1024 * 1024)

plt.figure(figsize=(15, 12))
# plot volsize sum per pool
ax1 = plt.subplot(321)
ax1 = volsperpool.plot(kind='bar', legend=False, ax=ax1, fontsize=12, grid=True)
ax1.set_ylabel('volsize sum (TB)')
ax1.set_xlabel('pools')
# plot space_total sum per pool
ax2 = plt.subplot(322)
ax2 = spacetperpool.plot(kind='bar', legend=False, ax=ax2, fontsize=12, grid=True)
ax2.set_ylabel('space total sum (TB)')
ax2.set_xlabel('pools')
# plot table for volsize sum per pool
ax3 = plt.subplot(323)
plt.axis('off')
tbl = table(ax3, volsperpool.round(2), loc='bottom', bbox=[0.2, 0.1, 0.5, 0.5])
tbl.auto_set_font_size(False)
tbl.set_fontsize(13)
# plot table for space_total sum per pool
ax4 = plt.subplot(324)
plt.axis('off')
tbl = table(ax4, spacetperpool.round(2), loc='bottom', bbox=[0.2, 0.1, 0.5, 0.5])
tbl.auto_set_font_size(False)
tbl.set_fontsize(13)
# plot pie volsize sum per pool
ax5 = plt.subplot(325)
ax5 = volsperpool.plot(kind='pie', legend=False, ax=ax5, subplots=True, startangle=90)
# plot pie volsize sum per pool
ax6 = plt.subplot(326)
ax6 = spacetperpool.plot(kind='pie', legend=False, ax=ax6, subplots=True, startangle=90)
plt.show()


# ### Get lun count per volsize

# In[ ]:


a = mydata.copy()
a.volsize = a.volsize / (1024 * 1024 * 1024)
groupsvolsize = a.groupby('volsize')
gvols = groupsvolsize.count()[['name']].rename(columns={'name': 'luns'})
def vertical_size(count):
    if count <= 25:
        return 10
    else:
        size = (count / 25) * 5
        if size <= 10:
            return 10
        else:
            return ((count / 25) * 5)

vertical = vertical_size(gvols.count()[0])
gvols.plot.barh(figsize=(18, vertical), grid=True)
plt.show()
gvols.sort_index(ascending=False)


# ## Get total usage from luns

# In[ ]:


usage = dataraw[['name', 'space_total', 'space_data', 'space_snapshots', 'space_available']]
total = usage.sum()[1:4]
display(Markdown("### Space Total: {}\n### Space Data: {}\n### Space Snapshots: {}"
                 .format(human_size(total.space_total), human_size(total.space_data),
                         human_size(total.space_snapshots))))


# In[ ]:


initiatorgrp = dataraw[['initiatorgroup', 'name']]
initiatorgrp.groupby('initiatorgroup').count().rename(columns={'name': 'lun count'})


# In[ ]:


initiators = initiatorgrp.groupby('initiatorgroup')
IGList = initiators.indices.keys()
ig = dataraw[['space_total', 'initiatorgroup']]
usage_per_ig = ig.groupby('initiatorgroup').sum()
for k, v in usage_per_ig.itertuples():
    display(Markdown("#### {}\n\nSize: **{}**".format(k.strip("[']"), human_size(v))))
    


# #### Get LUNs configured as thin provision (sparse)

# In[ ]:


sparse = dataraw[['name', 'sparse']]
luns_using_sparse = sparse.loc[sparse.sparse == True]
luns_not_using_sparse = sparse.loc[sparse.sparse == False]
display(Markdown("#### LUNs using thin provision: **{}**".format(luns_using_sparse['sparse'].count())))
display(Markdown("#### LUNs Not using thin provision: **{}**".format(luns_not_using_sparse['sparse'].count())))


# ### Get low use and overused luns assigned with thin provisioning
# 
# Low usage are lun with usage space less than 50% of the volsize, and over used lun is one that report a usage greater than the volsize.

# In[ ]:


sparse = dataraw[['name', 'project', 'pool', 'sparse', 'space_total', 'volsize']].set_index('name')
lusparse = sparse.loc[sparse.sparse == True].copy()
lusparse[['space_total', 'volsize']] = lusparse[['space_total', 'volsize']] / (1024 * 1024 * 1024)
low_use = lusparse.loc[(lusparse.space_total * 100) / lusparse.volsize <= 50 ]
over_use = lusparse.loc[(lusparse.space_total * 100) / lusparse.volsize >= 100 ]
display(Markdown("LUNs wasted: **{}**".format(low_use['sparse'].count())))
display(Markdown("LUNs overused: **{}**".format(over_use['sparse'].count())))
# Avoid SettingWithCopyWarning
pd.options.mode.chained_assignment = None
low_use.drop('sparse', axis=1, inplace=True)
over_use.drop('sparse', axis=1, inplace=True)
# enable SettingWithCopyWarning 
pd.options.mode.chained_assignment = 'warn'
plt.figure(figsize=(15, 8))
# plot bar
try:
    ax1 = plt.subplot(121)
    ax1 = low_use.plot(kind='bar', legend=True, ax=ax1, fontsize=12, grid=True)
    ax1.set_ylabel('Size (GB)')
    ax1.set_xlabel('Low use LUNs')
except:
    print("No low usage luns to plot")
# plot bar
try:
    ax2 = plt.subplot(122)
    ax2 = over_use.plot(kind='bar', legend=True, ax=ax2, fontsize=12, grid=True)
    ax2.set_ylabel('Size (GB)')
    ax2.set_xlabel('Overused LUNs')
except Exception as e:
    print("No overused luns to plot")
plt.show()


# ### Get LUNs using compression

# In[ ]:


compress = dataraw[['name', 'project', 'pool', 'compressratio']]
compress[compress['compressratio'] != 100]


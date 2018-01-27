# jupyter-zfssa-analysis

Jupyter Notebook to analyse my zfssa (ZFS Storage Appliance).

This notebooks needs the output from my zfs script explorer:

<https://github.com/aldenso/zfssa-scripts/tree/master/explorer>

After generating the explorer you can adjust the path in the notebooks to your unzipped explorers (default path: "/tmp/datazfssa").

## Using this repo with pip

Create a new virtualenv and activate it.

```sh
python -m venv jupytervenv
source jupytervenv/bin/activate
```

Clone the repo, change to the new directory and install the dependencies with the requirements file.

```sh
git clone https://github.com/aldenso/jupyter-zfssa-analysis
cd jupyter-zfssa-analysis
pip install -r requirements.txt
```

Enable the widgets.

```sh
jupyter nbextension enable --py widgetsnbextension --sys-prefix # use --sys-prefix when using virtualenvs
```

Now you can launch your jupyter notebook.

```sh
jupyter-notebook
```

## Using this repo with pipenv

If you don't have pipenv already installed, then proceed to install it with pip.

```sh
sudo pip install pipenv
```

With pipenv just clone the repo and change to the new directory, then run the install option.

```sh
git clone https://github.com/aldenso/jupyter-zfssa-analysis
cd jupyter-zfssa-analysis
pipenv install
```

Once all dependencies are installed then activate the virtualenv.

```sh
pipenv shell
```

Enable the widgets.

```sh
jupyter nbextension enable --py widgetsnbextension --sys-prefix # use --sys-prefix when using virtualenvs
```

Now you can launch your jupyter notebook.

```sh
jupyter-notebook
```

## Use this notebooks with a docker container if you prefer it

* step 1:

Clone this repo and change your working directory to it.

```sh
git clone https://github.com/aldenso/jupyter-zfssa-analysis
cd jupyter-zfssa-analysis
```

* step 2:

With Ipython, create a hashed password (if you want to change the password).

```python
In [1]: from notebook.auth import passwd
In [2]: passwd('password')
Out[2]: 'sha1:5b6fcd2f3bcc:acd703754a0dfaff49853f3233f395f50838ea7d'
```

* step 3:

If you decided to set a new password then change the hash in the Dockerfile.

```Dockerfile
# hashed password generated previously (check README)
ENV PASSWORD="'sha1:5b6fcd2f3bcc:acd703754a0dfaff49853f3233f395f50838ea7d'"

```

* step 4:

Build the image (it may take awhile) and validate if the new image is available.

```sh
$ sudo docker build -t yourname/archjupyter .

$ sudo docker images
REPOSITORY                 TAG                 IMAGE ID            CREATED             SIZE
aldenso/archjupyter        latest              95c1aa739366        About an hour ago   1.21GB
.
archlinux/base             latest              71415bf73a2b        3 weeks ago         394MB
.
```

* step 5:

Run a container and put some unzipped zfsssa explorer in the path shared to the container.

```sh
sudo docker run -d -v /tmp/datazfssa:/tmp/datazfssa -p 8888:8888 yourname/archjupyter
```

Now you can open your browser and test the notebooks (Remember to adjust the paths for the csv files).

```text
http://youripaddress:8888
```

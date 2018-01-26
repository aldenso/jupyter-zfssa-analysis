FROM archlinux/base

RUN pacman -Syu --noconfirm
RUN pacman -S --noconfirm python python-pip

# hashed password generated previously (check README)
ENV PASSWORD="'sha1:5b6fcd2f3bcc:acd703754a0dfaff49853f3233f395f50838ea7d'"

RUN useradd -ms /bin/bash juser
WORKDIR /home/juser

ADD . /home/juser
RUN pip install -r requirements.txt

# Make port 8888 available to the world outside this container
EXPOSE 8888

USER juser
WORKDIR /home/juser
RUN jupyter-notebook --generate-config
RUN sed -i "s/#c.NotebookApp.password = ''/c.NotebookApp.password = $PASSWORD/g" /home/juser/.jupyter/jupyter_notebook_config.py
ENTRYPOINT ["jupyter-notebook", "--notebook-dir=/home/juser", "--ip=0.0.0.0", "--port=8888", "--no-browser"]

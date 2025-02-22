FROM amazon/aws-lambda-python:3.12


RUN dnf install -y atk cups-libs gtk3 libXcomposite alsa-lib \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel nss mesa-libgbm jq unzip

COPY chrome-installer.sh /tmp/chrome-installer.sh

RUN chmod +x /tmp/chrome-installer.sh
RUN /tmp/chrome-installer.sh
RUN rm /tmp/chrome-installer.sh

COPY ./watcher/requirements.txt /tmp/
RUN python3 -m pip install --upgrade pip -q
RUN python3 -m pip install -r /tmp/requirements.txt -q 

COPY ./watcher/app.py ./

CMD ["app.lambda_handler"]

ARG CORE_VERSION=latest
FROM burger-war-core:$CORE_VERSION as system

ENV DEBIAN_FRONTEND=noninteractive

# 情報調査用のコマンドをインストール
RUN apt-get update -q && sudo apt-get install -y --no-install-recommends \
    lshw \
    kmod \
    lsof \
    && rm -rf /var/lib/apt/lists/*

#-------------------------------------------------------------------------------------------------
# VNC/デスクトップ環境のインストール
#-------------------------------------------------------------------------------------------------
################################################################################
# base system
################################################################################
RUN sed -i 's#http://archive.ubuntu.com/ubuntu/#mirror://mirrors.ubuntu.com/mirrors.txt#' /etc/apt/sources.list;

# built-in packages
ENV DEBIAN_FRONTEND noninteractive
RUN apt update \
    && apt install -y --no-install-recommends software-properties-common curl apache2-utils \
    && apt update \
    && apt install -y --no-install-recommends --allow-unauthenticated \
        supervisor nginx sudo net-tools zenity xz-utils \
        dbus-x11 x11-utils alsa-utils \
        mesa-utils libgl1-mesa-dri \
    && apt autoclean -y \
    && apt autoremove -y \
    && rm -rf /var/lib/apt/lists/*
# install debs error if combine together
RUN apt update \
    && apt install -y --no-install-recommends --allow-unauthenticated \
        xvfb x11vnc \
        vim-tiny firefox ttf-ubuntu-font-family ttf-wqy-zenhei  \
    && apt autoclean -y \
    && apt autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# RUN apt update \
#     && apt install -y gpg-agent \
#     && curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
#     && (dpkg -i ./google-chrome-stable_current_amd64.deb || apt-get install -fy) \
#     && curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add \
#     && rm google-chrome-stable_current_amd64.deb \
#     && rm -rf /var/lib/apt/lists/*

RUN apt update \
    && apt install -y --no-install-recommends --allow-unauthenticated \
        lxde gtk2-engines-murrine gnome-themes-standard gtk2-engines-pixbuf gtk2-engines-murrine arc-theme \
    && apt autoclean -y \
    && apt autoremove -y \
    && rm -rf /var/lib/apt/lists/*


# Additional packages require ~600MB
# libreoffice  pinta language-pack-zh-hant language-pack-gnome-zh-hant firefox-locale-zh-hant libreoffice-l10n-zh-tw

# tini to fix subreap
ARG TINI_VERSION=v0.18.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /bin/tini
RUN chmod +x /bin/tini

# ffmpeg
RUN apt update \
    && apt install -y --no-install-recommends --allow-unauthenticated \
        ffmpeg \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir /usr/local/ffmpeg \
    && ln -s /usr/bin/ffmpeg /usr/local/ffmpeg/ffmpeg

# python library
# COPY vnc/rootfs/usr/local/lib/web/backend/requirements.txt /tmp/
# RUN apt-get update \
#     && dpkg-query -W -f='${Package}\n' > /tmp/a.txt \
#     && apt-get install -y python3-pip python3-dev build-essential \
# 	&& pip3 install setuptools wheel && pip3 install -r /tmp/requirements.txt \
#     && ln -s /usr/bin/python3 /usr/local/bin/python \
#     && dpkg-query -W -f='${Package}\n' > /tmp/b.txt \
#     && apt-get remove -y `diff --changed-group-format='%>' --unchanged-group-format='' /tmp/a.txt /tmp/b.txt | xargs` \
#     && apt-get autoclean -y \
#     && apt-get autoremove -y \
#     && rm -rf /var/lib/apt/lists/* \
#     && rm -rf /var/cache/apt/* /tmp/a.txt /tmp/b.txt


################################################################################
# builder
################################################################################
# FROM burger-war-core:$CORE_VERSION as builder


# RUN sed -i 's#http://archive.ubuntu.com/ubuntu/#mirror://mirrors.ubuntu.com/mirrors.txt#' /etc/apt/sources.list;


# RUN apt-get update \
#     && apt-get install -y --no-install-recommends curl ca-certificates gnupg patch

# # nodejs
# RUN curl -sL https://deb.nodesource.com/setup_12.x | bash - \
#     && apt-get install -y nodejs

# # yarn
# RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
#     && echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list \
#     && apt-get update \
#     && apt-get install -y yarn

# # build frontend
# COPY vnc/web /src/web
# RUN cd /src/web \
#     && yarn \
#     && yarn build
# RUN sed -i 's#app/locale/#novnc/app/locale/#' /src/web/dist/static/novnc/app/ui.js


################################################################################
# merge
################################################################################
FROM system

# 日本語化
RUN apt-get update -q && sudo apt-get install -y \
    language-pack-ja-base \
    language-pack-ja \
    ibus-mozc \
    && rm -rf /var/lib/apt/lists/* \
    && localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

# gnome-terminalが起動しない対策
RUN echo "export LANG=ja_JP.UTF-8" >> /home/developer/.bashrc \
    && echo "export LANGUAGE=ja_JP:ja" >> /home/developer/.bashrc \
    && echo "export LC_ALL=ja_JP.UTF-8" >> /home/developer/.bashrc

# gnome-terminal起動時の以下の警告対策
# Couldn't register with accessibility busµ
RUN echo "NO_AT_BRIDGE=1" >> /home/developer/.bashrc

#COPY --from=builder /src/web/dist/ /usr/local/lib/web/frontend/
COPY vnc/rootfs /
# RUN ln -sf /usr/local/lib/web/frontend/static/websockify /usr/local/lib/web/frontend/static/novnc/utils/websockify && \
# 	chmod +x /usr/local/lib/web/frontend/static/websockify/run

WORKDIR /home/developer
#HEALTHCHECK --interval=30s --timeout=5s CMD curl --fail http://127.0.0.1:6079/api/health
ENTRYPOINT ["/entrypoint_vnc.sh"]

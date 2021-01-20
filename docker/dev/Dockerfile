FROM burger-war-core:latest

ARG DEBIAN_FRONTEND=noninteractive

# keyboard-configuarationのインストールで止まる為、予めインストールして設定
COPY ./dev/install-key-config.sh /install-key-config.sh
RUN sudo /install-key-config.sh

#-------------------------------------------------------------------------------------------------
# 開発PC用のドライバをインストールする
# （Gazeboが起動しない場合やGPUを使いたい場合は、ここで必要なドライバをインストールして下さい）
#-------------------------------------------------------------------------------------------------
# ubuntu-driversによる自動インストールの例
#-------------------------------------------------
# RUN sudo apt-get update -q && sudo apt-get install -y --no-install-recommends \
#     ubuntu-drivers-common \
#     && sudo rm -rf /var/lib/apt/lists/* \
#     && sudo ubuntu-drivers autoinstall

#===================================================================================
# PCやグラフィックボードによっては、ubuntu-driversが失敗する場合もあります。
# その場合、以下の例を参考に、開発PCにインストールされているバージョンのドライバを
# 個別にインストールして下さい。
#===================================================================================

# NVIDIAのドライバをインストールする例
#-------------------------------------------------
RUN sudo apt-get update -q && sudo apt-get install -y \
    nvidia-driver-450


# Intelのドライバをインストールする例
#-------------------------------------------------
# RUN sudo apt-get update -q && sudo apt-get install -y \
# 	i965-va-driver


#-------------------------------------------------------------------------------------------------
# 開発PCで使いたいツールなどをインストールする
#-------------------------------------------------------------------------------------------------
# RUN sudo apt-get update -q && sudo apt-get install -y --no-install-recommends \
#     x11-apps \
#     && sudo rm -rf /var/lib/apt/lists/*


#-------------------------------------------------------------------------------------------------
# 開発PCでの起動処理
#-------------------------------------------------------------------------------------------------
#COPY dev/mybash /mybash
#RUN sudo chown ${USERNAME}:${USERNAME} /mybash \
#    && sudo chmod +x /mybash

# 起動時の実行コマンドの指定
ENTRYPOINT [ "/entrypoint.sh" ]
CMD [ "/bash" ]

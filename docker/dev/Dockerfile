ARG CORE_VERSION=latest
FROM burger-war-core:$CORE_VERSION

ARG DEBIAN_FRONTEND=noninteractive

# keyboard-configurationのインストールが入力待ちで止まる為、予め自動でインストール
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
# RUN sudo apt-get update -q && sudo apt-get install -y \
#    nvidia-driver-450


# Intelのドライバをインストールする例
#-------------------------------------------------
# RUN sudo apt-get update -q && sudo apt-get install -y \
# 	i965-va-driver


#-------------------------------------------------------------------------------------------------
# 開発PCでのみ必要なツールのインストールや追加設定など
# ※シミュレーション対戦環境/実機環境でも必要な処理はdocker/core/Dockerfileに記載して下さい
#-------------------------------------------------------------------------------------------------
# RUN sudo apt-get update -q && sudo apt-get install -y --no-install-recommends \
#     x11-apps \
#     && sudo rm -rf /var/lib/apt/lists/*


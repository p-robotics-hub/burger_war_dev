FROM ghcr.io/p-robotics-hub/burger-war-kit:latest

#-------------------------------------------------------------------------------------------------
# シミュレーション環境/実機環境での実行に必要なパッケージをインストールする
#-------------------------------------------------------------------------------------------------

# RUN sudo apt-get install -y --no-install-recommends \
#     x11-apps \
#     && rm -rf /var/lib/apt/lists/*

# RUN yes | pip install \
#     requests \
#     flask

# 起動時の実行コマンドの指定
ENTRYPOINT [ "/entrypoint.sh" ]
CMD [ "bash" ]

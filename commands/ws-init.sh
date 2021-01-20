#!/bin/bash -eu
# Workspaceでcatkin_makeを実行する
# [USAGE]
#   docker-build.sh [-c docker build(コアイメージ用)に渡すオプション引数] [-d docker build(開発環境用)に渡すオプション引数] [-v Dockerイメージのバージョン]
CMD_NAME=`basename $0`
set -e
set -u

# 設定値読み込み
SCRIPT_DIR=$(cd "$(dirname $0)"; pwd)
source "${SCRIPT_DIR}/config.sh"

# Workspaceのディレクトリがない場合は作成
[ -d ${HOST_WS_DIR}/src ] || mkdir -p ${HOST_WS_DIR}/src

# Workspaceの作成と、ベースのgitリポジトリをcloneしビルド実施
docker exec -it  ${DEV_DOCKER_IMAGE_NAME} \
    /home/developer/scripts/ws-init.sh ${CONTAINER_WS_DIR}

echo "#--------------------------------------------------------------------"
echo "# ワークスペースを以下に作成しました"
echo "# PATH: ${HOST_WS_DIR}"
echo "#--------------------------------------------------------------------"


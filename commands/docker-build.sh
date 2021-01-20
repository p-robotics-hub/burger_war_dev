#!/bin/bash -eu
# Dockerfileのビルドスクリプト
# [USAGE]
#   docker-build.sh [-c docker build(コアイメージ用)に渡すオプション引数] [-d docker build(開発環境用)に渡すオプション引数] [-v Dockerイメージのバージョン]
CMD_NAME=`basename $0`

# 設定値読み込み
SCRIPT_DIR=$(cd "$(dirname $0)"; pwd)
source "${SCRIPT_DIR}/config.sh"

# オプション・引数解析
DEV_BUILD_OPTION=
CORE_BUILD_OPTION=
IMAGE_VERSION=latest
while getopts c:d:v: OPT
do
  case $OPT in
    "c" ) CORE_BUILD_OPTION="${CORE_BUILD_OPTION} ${OPTARG}" ;;
    "d" ) DEV_BUILD_OPTION="${DEV_BUILD_OPTION} ${OPTARG}" ;;
    "v" ) IMAGE_VERSION="${OPTARG}" ;;
      * ) echo "USAGE: ${CMD_NAME} [-d build-args(devel image)] [-l build-args(lib image)] [-v version]" 1>&2
          exit 1 ;;
  esac
done

# コアイメージ用のDockerfileのビルド
docker build ${CORE_BUILD_OPTION} \
  -f ${CORE_DOCKER_FILE_PATH} \
  -t ${CORE_DOCKER_IMAGE_NAME}:latest ${DOCKER_ROOT_DIR}

# 開発環境用のDockerfileのビルド
docker build ${DEV_BUILD_OPTION} \
  -f ${DEV_DOCKER_FILE_PATH} \
  -t ${DEV_DOCKER_IMAGE_NAME}:${IMAGE_VERSION} ${DOCKER_ROOT_DIR}

echo "#--------------------------------------------------------------------"
echo "# 以下のイメージを作成しました"
echo "# 本番環境用: ${CORE_DOCKER_IMAGE_NAME}:${IMAGE_VERSION}"
echo "# 開発環境用: ${DEV_DOCKER_IMAGE_NAME}:${IMAGE_VERSION}"
echo "#--------------------------------------------------------------------"

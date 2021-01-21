#!/bin/bash
###############################################################################
#-burger-war-core/burger-war-devのDockerfileをビルドする
#-
#+[USAGE]
#+  $0 [-a BUILDオプション(core/dev)] [-c BUILDオプション(core)] [-d BUILDオプション(dev)] [-v イメージのバージョン] [-h]
#+
#-[OPTIONS]
#-  -a options    burger-war-core/burger-war-devの'docker build'に追加で渡す引数を指定（複数回指定可能）
#-  -c options    burger-war-coreの'docker build'に追加で渡す引数を指定（複数回指定可能）
#-  -d options    burger-war-devの'docker build'に追加で渡す引数を指定（複数回指定可能）
#-  -v version    'docker build -t'で指定するイメージのバージョンを指定 (default: latest)
#-  -h            このヘルプを表示
#-
###############################################################################
set -e
set -u
CMD_NAME=$(basename $0)

# 関数定義
#------------------------------------------------
usage_exit() {
  # ファイル冒頭のコメントからUSAGEを出力
  sed '/^[^#]/q' "$0"             \
  | sed -n '/^#+/s/^#+//p'        \
  | sed "s/\$0/${CMD_NAME}/g"     1>&2
  exit 1
}
help_exit() {
  # ファイル冒頭のコメントからヘルプを出力
  sed '/^[^#]/q' "$0"             \
  | sed -n '/^#[-+]/s/^#[-+]//p'  \
  | sed "s/\$0/${CMD_NAME}/g"     1>&2
  exit 0
}

# 設定値読み込み
#------------------------------------------------
SCRIPT_DIR=$(cd "$(dirname $0)"; pwd)
source "${SCRIPT_DIR}/config.sh"


# オプション・引数解析
#------------------------------------------------
DEV_BUILD_OPTION=
CORE_BUILD_OPTION=
IMAGE_VERSION=latest
while getopts a:c:d:v:h OPT
do
  case $OPT in
    a  ) # burger-war-core/burger-war-devのdocker buildへの追加オプション引数指定
      CORE_BUILD_OPTION="${CORE_BUILD_OPTION} ${OPTARG}"
      DEV_BUILD_OPTION="${DEV_BUILD_OPTION} ${OPTARG}"
      ;;
    c  ) # burger-war-coreのdocker buildへの追加オプション引数指定
      CORE_BUILD_OPTION="${CORE_BUILD_OPTION} ${OPTARG}"
      ;;
    d  ) # burger-war-devのdocker buildへの追加オプション引数指定
      DEV_BUILD_OPTION="${DEV_BUILD_OPTION} ${OPTARG}"
      ;;
    v  ) # Dockerイメージのバージョン指定
      IMAGE_VERSION="${OPTARG}"
      ;;
    h  ) # ヘルプの表示
      help_exit
      ;;
    \? ) # 不正オプション時のUSAGE表示
      usage_exit
      ;;
  esac
done
shift $((OPTIND - 1))

# コアイメージ用のDockerfileのビルド
#------------------------------------------------
set -x
docker build ${CORE_BUILD_OPTION} \
  -f ${CORE_DOCKER_FILE_PATH} \
  -t ${CORE_DOCKER_IMAGE_NAME}:${IMAGE_VERSION} ${DOCKER_ROOT_DIR}
set +x

# 開発環境用のDockerfileのビルド
#------------------------------------------------
set -x
docker build ${DEV_BUILD_OPTION} \
  -f ${DEV_DOCKER_FILE_PATH} \
  -t ${DEV_DOCKER_IMAGE_NAME}:${IMAGE_VERSION} ${DOCKER_ROOT_DIR}
set +x

echo "#--------------------------------------------------------------------"
echo "# 以下のイメージを作成しました"
echo "# カスタマイズ用: ${CORE_DOCKER_IMAGE_NAME}:${IMAGE_VERSION}"
echo "# 開発環境用　　: ${DEV_DOCKER_IMAGE_NAME}:${IMAGE_VERSION}"
echo "#--------------------------------------------------------------------"

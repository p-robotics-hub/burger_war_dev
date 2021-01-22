#!/bin/bash
###############################################################################
#-ワークスペースのビルド(catkin_make)を実行する
#-
#+[USAGE]
#+  $0 [-a EXECオプション] [-h] -- [catkin_makeオプション]
#+
#-[OPTIONS]
#-  -a options    'docker exec'に追加で渡す引数を指定（複数回指定可能）
#-  -h            このヘルプを表示
#-
#-[ARGUMENTS]
#-  options       catkin_makeに渡す引数
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
EXEC_OPTION=
IMAGE_VERSION=latest
while getopts a:h OPT
do
  case $OPT in
    a  ) # docker execへの追加オプション引数指定
      EXEC_OPTION="${EXEC_OPTION} ${OPTARG}"
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
MAKE_OPTION="$@"

# ワークスペースのビルド
#------------------------------------------------
docker exec \
  -it \
  --user $(id -u) \
  ${EXEC_OPTION} \
  ${DEV_DOCKER_CONTAINER_NAME} \
  bash -l -c "ws-build.sh -w ${CONTAINER_WS_DIR} -- ${MAKE_OPTION}"
 
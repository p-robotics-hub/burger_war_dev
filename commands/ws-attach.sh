#!/bin/bash
###############################################################################
#-burger-war-devのコンテナからbashを起動する
#-
#+[USAGE]
#+  $0 [-a EXECオプション] [-c bashオプション] [-h]
#+
#-[OPTIONS]
#-  -a options    'docker exec'に追加で渡す引数を指定（複数回指定可能）
#-  -c command    'bash -c'に渡す引数を指定
#-  -h            このヘルプを表示
#-
#-[ARGUMENTS]
#-  options       bash起動時に渡す引数
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
BASH_ARGS=
IMAGE_VERSION=latest
while getopts a:c:h OPT
do
  case $OPT in
    a  ) # docker execへの追加オプション引数指定
      EXEC_OPTION="${EXEC_OPTION} ${OPTARG}"
      ;;
    c  ) # bashに渡すオプション引数指定
      BASH_ARGS="-l -c ${OPTARG}"
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

# 対話モードでbashを起動
#------------------------------------------------
echo "#--------------------------------------------------------------------"
echo "# 以下のコンテナでbashを起動します"
echo "# CONTAINER NAME: ${DEV_DOCKER_CONTAINER_NAME}"
echo "# EXEC COMMAND  : bash ${BASH_ARGS}"
echo "#--------------------------------------------------------------------"
docker exec \
  -it \
  ${EXEC_OPTION} \
  ${DEV_DOCKER_CONTAINER_NAME} \
  bash ${BASH_ARGS}

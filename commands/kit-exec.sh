#!/bin/bash
###############################################################################
#-開発用コンテナ上でburger-war-kitディレクトリに移動してコマンドを実行する
#-
#+[USAGE]
#+  $0 [-a EXECオプション] [-s] [-h] -- 実行コマンド
#+
#-[OPTIONS]
#-  -a options    'docker exec'に追加で渡す引数を指定（複数回指定可能）
#-  -s            burger-war-kit/scripts/以下のスクリプトを実行する
#-  -h            このヘルプを表示
#-
#-[ARGUMENTS]
#-  script-name  実行するスクリプト名を指定する
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
EXEC_COMMAND=
while getopts a:sh OPT
do
  case $OPT in
    a  ) # docker execへの追加オプション引数指定
      EXEC_OPTION="${EXEC_OPTION} ${OPTARG}"
      ;;
    s  ) # docker execへの追加オプション引数指定
      EXEC_COMMAND="bash scripts/"
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

EXEC_COMMAND="${EXEC_COMMAND}$@"

# 対話モードでbashを起動
#------------------------------------------------
cat <<-EOM
#--------------------------------------------------------------------
# 以下のコンテナで'${EXEC_COMMAND}'を実行します
# CONTAINER NAME: ${DEV_DOCKER_CONTAINER_NAME}
#--------------------------------------------------------------------
EOM

docker exec \
  -it \
  --user $(id -u) \
  ${EXEC_OPTION} \
  ${DEV_DOCKER_CONTAINER_NAME} \
  bash -l -c "cd ${CONTAINER_WS_DIR}/src/burger_war_kit && ${EXEC_COMMAND}"

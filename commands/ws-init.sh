#!/bin/bash
###############################################################################
#-ワークスペース作成(catkin_init_workspace)とビルド(catkin_make)を実行する
#-
#+[USAGE]
#+  $0 [-a EXECオプション] [-h]
#+
#-[OPTIONS]
#-  -a options    'docker exec'に追加で渡す引数を指定（複数回指定可能）
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
EXEC_OPTION=
IMAGE_VERSION=latest
while getopts a:v:w:h OPT
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

# 既にワークスペースが存在する場合は、ユーザーに確認して削除
#------------------------------------------------
if [ -L "${HOST_WS_DIR}/src/CMakeLists.txt" ]; then
  echo "${HOST_WS_DIR}/src/CMakeLists.txtは既に存在します。"
  read -p "削除して再度ワークスペースの初期化を行いますか？(yes/no): " yesno
  case "$yesno" in
    yes ) rm -vf "${HOST_WS_DIR}/.catkin_workspace"
          rm -vf "${HOST_WS_DIR}/src/CMakeLists.txt"
          rm -vrf "${HOST_WS_DIR}/build"
          rm -vrf "${HOST_WS_DIR}/devel"
          echo "古いワークスペースを削除しました"
          ;;
      * ) echo "ワークスペースの作成を中断しました。"
          exit 1
          ;;
  esac
fi

# ワークスペースの作成とビルド
#------------------------------------------------
docker exec \
  -it \
  --user $(id -u) \
  ${EXEC_OPTION} \
  ${DEV_DOCKER_CONTAINER_NAME} \
  bash -l -c "ws-init.sh -w ${CONTAINER_WS_DIR}"

cat <<-EOM
#--------------------------------------------------------------------
# ワークスペースを以下に作成しました
# PATH(host)  : ${HOST_WS_DIR}
# PATH(docker): ${CONTAINER_WS_DIR}
#--------------------------------------------------------------------
EOM


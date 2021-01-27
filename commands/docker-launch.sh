#!/bin/bash
###############################################################################
#-burger-war-kitのDockerコンテナを起動する
#-
#+[USAGE]
#+  $0 [-a RUNオプション] [-v イメージのバージョン] [-w WSディレクトリ][-h]
#+
#-[OPTIONS]
#-  -a options    'docker run'に追加で渡す引数を指定（複数回指定可能）
#-  -r            リモートデスクトップモード(VNC)として起動
#-  -w dir-path   ホストPCのロボコンワークスペースのパスを指定 (default: $HOME/catkin_ws)
#-  -v version    'docker run'で起動するイメージの'version'を指定 (default: latest)
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
RUN_OPTION=
IMAGE_VERSION=latest
VNC_MODE=
while getopts a:v:w:rh OPT
do
  case $OPT in
    a  ) # docker runへの追加オプション引数指定
      RUN_OPTION="${RUN_OPTION} ${OPTARG}"
      ;;
    w  ) # ホストのワークスペースの指定
      HOST_WS_DIR="${OPTARG}"
      ;;
    v  ) # Dockerイメージのバージョン指定
      IMAGE_VERSION="${OPTARG}"
      ;;
    r  ) # VNCモードで起動
      VNC_MODE=1
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

# 同名のコンテナが存在する場合は停止する
#------------------------------------------------
if docker container ls --format '{{.Names}}' | grep -q -e "^${DEV_DOCKER_CONTAINER_NAME}$" ; then
  echo "起動中の ${DEV_DOCKER_CONTAINER_NAME} コンテナを停止します..."
  docker container stop ${DEV_DOCKER_CONTAINER_NAME} >/dev/null
  echo "起動中の ${DEV_DOCKER_CONTAINER_NAME} コンテナを停止しました"
fi

# 同名のコンテナが存在する場合は削除する
#------------------------------------------------
if docker container ls -a --format '{{.Names}}' | grep -q -e "^${DEV_DOCKER_CONTAINER_NAME}$" ; then
  echo -e "\e[33mWARNING: 前回起動していた ${DEV_DOCKER_CONTAINER_NAME} コンテナが存在します"
  read -p "既存のコンテナを削除して、新しいコンテナを起動しますか？(yes/no): " yesno
  echo -e "\e[m"
  case $yesno in
    yes ) # 既存のコンテナ
      echo "既存の ${DEV_DOCKER_CONTAINER_NAME} コンテナを削除します..."
      docker rm ${DEV_DOCKER_CONTAINER_NAME} >/dev/null
      echo "既存の ${DEV_DOCKER_CONTAINER_NAME} コンテナを削除しました"
      ;;
    * ) # 既存のコンテナを別名で保存
      read -p "既存のコンテナをイメージとして保存します。保存するバージョン名を入力して下さい: " backup_version
      if [ -z "${backup_version}" ]; then
        echo "バージョン名が不正です。起動処理を中断します"
      fi
      docker commit ${DEV_DOCKER_CONTAINER_NAME} ${DEV_DOCKER_IMAGE_NAME}:${backup_version} >/dev/null
      echo -e "\e[33m#--------------------------------------------------------------------"
      echo -e "# 既存のコンテナを以下のイメージとして保存しました"
      echo -e "# SAVE IMAGE NAME: ${DEV_DOCKER_IMAGE_NAME}:${backup_version}"
      echo -e "# "
      echo -e "# 保存したイメージからコンテナを起動するには、以下のコマンドを実行して下さい"
      echo -e "# RUN COMMAND    : bash commands/docker-launch.sh -v ${backup_version}"
      echo -e "#--------------------------------------------------------------------\e[m"
      docker rm ${DEV_DOCKER_CONTAINER_NAME} >/dev/null
      ;;
  esac
fi

# 新たにコンテナを起動する
#------------------------------------------------
if [ -z "$VNC_MODE"]; then
  set -x
  docker run \
    --name ${DEV_DOCKER_CONTAINER_NAME} \
    -d \
    --privileged \
    --net host \
    --mount type=bind,src=/tmp/.X11-unix/,dst=/tmp/.X11-unix \
    --mount type=bind,src=${HOST_WS_DIR},dst=${CONTAINER_WS_DIR} \
    --device /dev/snd \
    -e DISPLAY=${DISPLAY} \
    -e HOST_USER_ID=$(id -u) \
    -e HOST_GROUP_ID=$(id -g) \
    ${RUN_OPTION} \
    ${DEV_DOCKER_IMAGE_NAME}:${IMAGE_VERSION} \
    tail -f /dev/null
  set +x
else
  set -x
  docker run \
    --name ${DEV_DOCKER_CONTAINER_NAME} \
    -d \
    --privileged \
    --mount type=bind,src=${HOST_WS_DIR},dst=${CONTAINER_WS_DIR} \
    --device /dev/snd \
    -e DISPLAY=${DISPLAY} \
    -e HOST_USER_ID=$(id -u) \
    -e HOST_GROUP_ID=$(id -g) \
    -p 5901:5901 \
    ${RUN_OPTION} \
    ${DEV_DOCKER_IMAGE_NAME}:${IMAGE_VERSION} \
    'export USER=developer && vncserver :1 -geometry 1280x800 -depth 24 && tail -f /home/developer/.vnc/*:1.log
'
  set +x
fi
cat <<-EOM
#--------------------------------------------------------------------
# 開発用のコンテナを起動しました
# USE IMAGE NAME: ${DEV_DOCKER_IMAGE_NAME}:${IMAGE_VERSION}
# CONTAINER NAME: ${DEV_DOCKER_IMAGE_NAME}
#--------------------------------------------------------------------
EOM

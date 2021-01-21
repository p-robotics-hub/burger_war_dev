#----------------------------------------------------------
# Repository config values
#----------------------------------------------------------
# GitHubのユーザ名
GITHUB_USER=$(git config user.email)

# Dockerイメージを登録するレジストリのURL
REGISTRY_ROOT=ghcr.io
REGISTRY_URL=${REGISTRY_ROOT}/$(echo "${GITHUB_USER}" | sed -e 's/\(.*\)/\L\1/')

# Dockerイメージ名(公開パッケージ名)
DOCKER_IMAGE_NAME=burger-war

# Dockerイメージ名(ローカルパッケージ名)
CORE_DOCKER_IMAGE_NAME=burger-war-core
DEV_DOCKER_IMAGE_NAME=burger-war-dev
DEV_DOCKER_CONTAINER_NAME=${DEV_DOCKER_IMAGE_NAME}

#----------------------------------------------------------
# Local config values
#----------------------------------------------------------
# GitHubのPersonal access tokensを保存したファイルのパス
GITHUB_TOKEN_FILE=${HOME}/.github-token

# ワークスペースのrootディレクトリのパス
HOST_WS_DIR=${HOME}/catkin_ws
# コンテナ上のワークスペースディレクトリ
CONTAINER_WS_DIR=/home/developer/catkin_ws

# kit/devのrootディレクトリパス
BURGER_WAR_KIT_DIR=${HOST_WS_DIR}/src/burger_war_kit
BURGER_WAR_DEV_DIR=${HOST_WS_DIR}/src/burger_war_dev

# ビルドするDockerfileパス
DOCKER_ROOT_DIR=${BURGER_WAR_DEV_DIR}/docker
CORE_DOCKER_FILE_PATH=${DOCKER_ROOT_DIR}/core/Dockerfile
DEV_DOCKER_FILE_PATH=${DOCKER_ROOT_DIR}/dev/Dockerfile


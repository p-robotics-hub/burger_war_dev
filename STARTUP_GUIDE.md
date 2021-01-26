# Startup Guide of burger_war
burger_warの開発環境を構築する手順について説明します。

## 目次

<!-- TOC -->

- [目次](#%E7%9B%AE%E6%AC%A1)
- [インストール](#%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB)
    - [このリポジトリのクローン](#%E3%81%93%E3%81%AE%E3%83%AA%E3%83%9D%E3%82%B8%E3%83%88%E3%83%AA%E3%81%AE%E3%82%AF%E3%83%AD%E3%83%BC%E3%83%B3)
    - [Dockerのインストール](#docker%E3%81%AE%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB)
- [開発用のDockerイメージの作成](#%E9%96%8B%E7%99%BA%E7%94%A8%E3%81%AEdocker%E3%82%A4%E3%83%A1%E3%83%BC%E3%82%B8%E3%81%AE%E4%BD%9C%E6%88%90)
    - [開発用のDockerイメージの作成](#%E9%96%8B%E7%99%BA%E7%94%A8%E3%81%AEdocker%E3%82%A4%E3%83%A1%E3%83%BC%E3%82%B8%E3%81%AE%E4%BD%9C%E6%88%90)
    - [カスタマイズしたDockerイメージの作成](#%E3%82%AB%E3%82%B9%E3%82%BF%E3%83%9E%E3%82%A4%E3%82%BA%E3%81%97%E3%81%9Fdocker%E3%82%A4%E3%83%A1%E3%83%BC%E3%82%B8%E3%81%AE%E4%BD%9C%E6%88%90)
        - [Dockerfileの修正例](#dockerfile%E3%81%AE%E4%BF%AE%E6%AD%A3%E4%BE%8B)
        - [バージョンを指定してDockerイメージを作成する](#%E3%83%90%E3%83%BC%E3%82%B8%E3%83%A7%E3%83%B3%E3%82%92%E6%8C%87%E5%AE%9A%E3%81%97%E3%81%A6docker%E3%82%A4%E3%83%A1%E3%83%BC%E3%82%B8%E3%82%92%E4%BD%9C%E6%88%90%E3%81%99%E3%82%8B)
- [開発用のDockerコンテナの起動](#%E9%96%8B%E7%99%BA%E7%94%A8%E3%81%AEdocker%E3%82%B3%E3%83%B3%E3%83%86%E3%83%8A%E3%81%AE%E8%B5%B7%E5%8B%95)
    - [バージョンを指定せずにコンテナを起動](#%E3%83%90%E3%83%BC%E3%82%B8%E3%83%A7%E3%83%B3%E3%82%92%E6%8C%87%E5%AE%9A%E3%81%9B%E3%81%9A%E3%81%AB%E3%82%B3%E3%83%B3%E3%83%86%E3%83%8A%E3%82%92%E8%B5%B7%E5%8B%95)
        - [Gazeboが起動しない場合](#gazebo%E3%81%8C%E8%B5%B7%E5%8B%95%E3%81%97%E3%81%AA%E3%81%84%E5%A0%B4%E5%90%88)
    - [バージョンを指定してコンテナを起動](#%E3%83%90%E3%83%BC%E3%82%B8%E3%83%A7%E3%83%B3%E3%82%92%E6%8C%87%E5%AE%9A%E3%81%97%E3%81%A6%E3%82%B3%E3%83%B3%E3%83%86%E3%83%8A%E3%82%92%E8%B5%B7%E5%8B%95)
- [ワークスペースのビルド](#%E3%83%AF%E3%83%BC%E3%82%AF%E3%82%B9%E3%83%9A%E3%83%BC%E3%82%B9%E3%81%AE%E3%83%93%E3%83%AB%E3%83%89)
- [シミュレーションの実行](#%E3%82%B7%E3%83%9F%E3%83%A5%E3%83%AC%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3%E3%81%AE%E5%AE%9F%E8%A1%8C)
    - [審判サーバーを立ち上げずにシミュレータとロボットのみ立ち上げる場合](#%E5%AF%A9%E5%88%A4%E3%82%B5%E3%83%BC%E3%83%90%E3%83%BC%E3%82%92%E7%AB%8B%E3%81%A1%E4%B8%8A%E3%81%92%E3%81%9A%E3%81%AB%E3%82%B7%E3%83%9F%E3%83%A5%E3%83%AC%E3%83%BC%E3%82%BF%E3%81%A8%E3%83%AD%E3%83%9C%E3%83%83%E3%83%88%E3%81%AE%E3%81%BF%E7%AB%8B%E3%81%A1%E4%B8%8A%E3%81%92%E3%82%8B%E5%A0%B4%E5%90%88)
- [起動したコンテナの中で操作をしたい場合](#%E8%B5%B7%E5%8B%95%E3%81%97%E3%81%9F%E3%82%B3%E3%83%B3%E3%83%86%E3%83%8A%E3%81%AE%E4%B8%AD%E3%81%A7%E6%93%8D%E4%BD%9C%E3%82%92%E3%81%97%E3%81%9F%E3%81%84%E5%A0%B4%E5%90%88)
- [短縮コマンドの設定例](#%E7%9F%AD%E7%B8%AE%E3%82%B3%E3%83%9E%E3%83%B3%E3%83%89%E3%81%AE%E8%A8%AD%E5%AE%9A%E4%BE%8B)
- [Dockerfileの構成について](#dockerfile%E3%81%AE%E6%A7%8B%E6%88%90%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6)
- [グラフィックボードのドライバの補足](#%E3%82%B0%E3%83%A9%E3%83%95%E3%82%A3%E3%83%83%E3%82%AF%E3%83%9C%E3%83%BC%E3%83%89%E3%81%AE%E3%83%89%E3%83%A9%E3%82%A4%E3%83%90%E3%81%AE%E8%A3%9C%E8%B6%B3)
    - [ホストPCが利用中のドライバの確認方法](#%E3%83%9B%E3%82%B9%E3%83%88pc%E3%81%8C%E5%88%A9%E7%94%A8%E4%B8%AD%E3%81%AE%E3%83%89%E3%83%A9%E3%82%A4%E3%83%90%E3%81%AE%E7%A2%BA%E8%AA%8D%E6%96%B9%E6%B3%95)
    - [NVIDIAの場合](#nvidia%E3%81%AE%E5%A0%B4%E5%90%88)
        - [Ubuntuの標準バージョンのドライバのインストール](#ubuntu%E3%81%AE%E6%A8%99%E6%BA%96%E3%83%90%E3%83%BC%E3%82%B8%E3%83%A7%E3%83%B3%E3%81%AE%E3%83%89%E3%83%A9%E3%82%A4%E3%83%90%E3%81%AE%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB)
        - [詳細なバージョンを指定してインストール](#%E8%A9%B3%E7%B4%B0%E3%81%AA%E3%83%90%E3%83%BC%E3%82%B8%E3%83%A7%E3%83%B3%E3%82%92%E6%8C%87%E5%AE%9A%E3%81%97%E3%81%A6%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB)
    - [Intelの場合](#intel%E3%81%AE%E5%A0%B4%E5%90%88)
    - [AMD/ATIの場合](#amdati%E3%81%AE%E5%A0%B4%E5%90%88)
    - [グラフィックスドライバ関連の参考サイト](#%E3%82%B0%E3%83%A9%E3%83%95%E3%82%A3%E3%83%83%E3%82%AF%E3%82%B9%E3%83%89%E3%83%A9%E3%82%A4%E3%83%90%E9%96%A2%E9%80%A3%E3%81%AE%E5%8F%82%E8%80%83%E3%82%B5%E3%82%A4%E3%83%88)
- [その他](#%E3%81%9D%E3%81%AE%E4%BB%96)
    - [PROXYの設定について](#proxy%E3%81%AE%E8%A8%AD%E5%AE%9A%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6)

<!-- /TOC -->


<br />

## インストール
burger_warの開発に必要なツールをインストールします。

### このリポジトリのクローン
--------------------------------------------------------------------
まずは、gitとcurlをインストールします。

```
sudo apt-get install -y git curl
```

次にワークスペースディレクトリを作成し、本リポジトリと開発ツール用のリポジトリをクローンします。

[TODO:mainマージ後に’-b with_docker ’を削除する]

```
mkdir -p ~/catkin_ws/src && cd ~/catkin_ws/src
git clone -b with_docker https://github.com/p-robotics-hub/burger_war_dev
git clone -b with_docker https://github.com/p-robotics-hub/burger_war_kit
```

実行後のディレクトリ構成は以下となります。

```
~/catkin_ws/src/
|-- burger_war_dev/
|-- burger_war_kit/
```

<br />

### Dockerのインストール
--------------------------------------------------------------------

docker engineとdocker-composeをインストールします。
※既にインストール済みの方は、本手順はスキップして下さい

まずは、以下のコマンドでディレクトリを移動して下さい。

```
cd ~/catkin_ws/src/burger_war_dev
```

開発用パソコンのOSがUbuntuで、CPUがx86_64かamd64の場合、コマンドを実行して下さい。

```
bash commands/docker-install.sh amd64
```

もし、CPUが ARM32bit か ARM64bit の環境にインストールする場合は、`amd64`の代わりに以下の引数を指定して下さい。

```
bash commands/docker-install.sh armhf       # ARM32bit環境の場合
bash commands/docker-install.sh arm64       # ARM64bit環境の場合
```

Ubuntu以外のLinuxディストリビューションの場合は、以下の公式の手順を参照して下さい。

- [dockerのインストール](https://docs.docker.com/engine/install/)
- [docker-composeのインストール](https://docs.docker.com/compose/install/)


<span style="color: red;">インストール完了後、一度パソコンを再起動して下さい。</span>


<br />

## 開発用のDockerイメージの作成

Dockerのインストールが終わったら、開発環境用のDockerイメージを作成します。

以下のコマンドでディレクトリを移動してから、以降の手順を実施して下さい。

```
cd ~/catkin_ws/src/burger_war_dev
```

### 開発用のDockerイメージの作成
--------------------------------------------------------------------

まずは、cloneした素の状態でDockerイメージを作成してみましょう。

以下のコマンドを実行して下さい。

```
bash commands/docker-build.sh
```

ビルドに成功したら、以下のように2つのDockerイメージが生成されます。

```
#--------------------------------------------------------------------
# 以下のイメージを作成しました
# カスタマイズ用: burger-war-core:latest
# 開発環境用　　: burger-war-dev:latest
#--------------------------------------------------------------------
```

上記では`burger-war-dev:latest`というDockerイメージが作成されたことが確認できます。

`:`より前がDockerのイメージ名、`:`以降はDockerイメージのバージョンになっていて、バージョンはデフォルトでは最新であることを示す「latest」になります。  
（別のバージョンでイメージを作成する方法は後述します）

ビルドが終わったら、[バージョンを指定せずにコンテナを起動](#バージョンを指定せずにコンテナを起動)の手順に従って、コンテナを起動して動作確認をして下さい。

<br />

### カスタマイズしたDockerイメージの作成
--------------------------------------------------------------------

Gazeboの起動に失敗したり、ロボコンで使用したい追加ライブラリなどがある場合、カスタマイズしたDockerイメージの作成が必要になります。

具体的には、以下の2つのDockerfileを修正します。

```
burger_war_dev
|-- docker
|   |-- core
|   |   |-- Dockerfile    シミュレーション対戦/実機環境で使用したいライブラリのインストールなどを追記する
|   |-- dev
|   |   |-- Dockerfile    開発用パソコンに必要なドライバやツールのインストール、設定などを追記する
```

<br />

#### Dockerfileの修正例

##### ライブラリをインストールする場合
ロボコン用に作成するプログラムで使いたいライブラリがある場合、`docker/core/Dockerfile`に必要なインストール処理を追加して下さい。

###### apt-get
apt-getでインストールする場合の例は、以下になります。  

```
# apt-getで必要なパッケージをインストールする例
#-------------------------------------------------
RUN apt-get update -q && apt-get install -y --no-install-recommends \
    ros-${ROS_DISTRO}-dwa-local-planner \
    ros-${ROS_DISTRO}-global-planner \
    libarmadillo-dev \
    libarmadillo8 \
    && rm -rf /var/lib/apt/lists/*
```

`ros-${ROS_DISTRO}-dwa-local-planner \`などを、必要なパッケージ名に置き換えて下さい。  
※`${ROS_DISTRO}`の実際の値は`melodic`となります。

Dockerfileを変更したらファイルを保存後、ビルドしてコンテナを起動して下さい。

```
bash commands/docker-build.sh
bash commands/docker-launch.sh
```

インストールできているか確認するには、以下のコマンドを実行して下さい。

```
bash commands/kit.sh -c apt list インストールしたパッケージ名
```

例えば「ros-${ROS_DISTRO}-dwa-local-planner」がインストールされたか確認する場合は、以下となります。  
最後の行から、バージョンは「1.16.7」であることが分かります。

```
$ bash commands/kit.sh -c apt list ros-*-global-planner
#--------------------------------------------------------------------
# 以下のコンテナでコマンドを実行します
# CONTAINER NAME: burger-war-dev
# EXEC COMMAND  : bash -l -c apt list ros-*-global-planner
#--------------------------------------------------------------------
++ id -u
+ docker exec -it --user 1000 burger-war-dev bash -l -c 'apt list ros-*-global-planner'
Listing... Done
ros-melodic-global-planner/now 1.16.7-1bionic.20201103.003153 amd64 [installed,local]
```

###### pip
pipでインストールする場合の例は、以下となります。  
`transitions \`などを、必要なパッケージ名に置き換えて下さい。(最後の行には`\`は不要です)  

```
# pipで必要なパッケージをインストールする例
#-------------------------------------------------
RUN yes | pip install \
    transitions \
    pygraphviz
```

Dockerfileを変更したらファイルを保存後、ビルドしてコンテナを起動して下さい。

```
bash commands/docker-build.sh
bash commands/docker-launch.sh
```

インストールできているか確認するには、以下のコマンドを実行して下さい。

```
bash commands/kit.sh -c pip list | grep transitions
```

インストールされている場合、以下のようにパッケージ名とバージョンが出力されます。

```
++ id -u
+ docker exec -it --user 1000 burger-war-dev bash -l -c 'pip list'
transitions                   0.8.6
```

###### ホストPCで用意した実行ファイルをインストールする場合
ホストPCで用意した実行ファイルやスクリプトなどをインストールするには、DockerfileのCOPY命令でPATHが通ったディレクトリにコピーして下さい。  

例えば、`docker/core/myexec`以下にコピーする実行ファイルを用意した場合、以下のような記載になります。
(インストール先の`/usr/local/bin/myexec`は、必要であれば置き換えて下さい)

```
COPY core/myexec /usr/local/bin/myexec
RUN chmod +x /usr/local/bin/myexec
```

Dockerfileを変更したらファイルを保存後、ビルドしてコンテナを起動して下さい。

```
bash commands/docker-build.sh
bash commands/docker-launch.sh
```

動作確認はインストールしたものに合わせて実施して下さい。
PATHが通った場所にインストールできていれば、以下のような形で実行できます。

```
bash commands/kit.sh -c myexec
```

##### 開発環境に必要なパッケージ(ドライバなど)をインストールする場合
開発用のパソコンでのみ使いたいツールや、ドライバがある場合、`docker/dev/Dockerfile`に必要なインストール処理を追加して下さい。

ここでは、Gazeboが起動しなかった為、グラフィックボードのドライバをインストールする場合を想定して説明します。

Ubuntuには対応するドライバを自動で検出してインストールする`ubuntu-drivers`というツールが用意されています。  
Gazeboが起動しないときは、まずはこれを試してみましょう。

`docker/dev/Dokcerfile`の以下の箇所から行頭の#を削除して下さい。

```
# ubuntu-driversによる自動インストールの例
#-------------------------------------------------
RUN apt-get update -q && apt-get install -y --no-install-recommends \
    ubuntu-drivers-common \
    && rm -rf /var/lib/apt/lists/* \
    && ubuntu-drivers autoinstall
```

Dockerfileの修正が終わったらファイルを保存し、以下のコマンドでビルドして下さい。

```
bash commands/docker-build.sh
```

ビルドが終わったら、[バージョンを指定せずにコンテナを起動](#バージョンを指定せずにコンテナを起動)の手順に従って、コンテナを起動してが起動するか確認をして下さい。

もしGazeboが起動しない場合は、[グラフィックボードのドライバの補足](#グラフィックボードのドライバの補足)を参考に、ホストPCと同じドライバをインストールして試して下さい。

<br />

#### バージョンを指定してDockerイメージを作成する
Dockerfileを修正したら、ビルドするにはデフォルト状態のビルドと同じコマンドを使います。  
生成されるDockerイメージ名とバージョンも同じになります。

```
bash commands/docker-build.sh
```

もし、バージョンを変えたDockerイメージを作成したい場合は、以下のように`-v`オプションでバージョンを指定して下さい。

```
bash commands/docker-build.sh -v test
```

ビルドに成功したら以下のようなメッセージが出力され、`test`というバージョンののDockerイメージが作成されたことが確認できます。 

```
#--------------------------------------------------------------------
# 以下のイメージを作成しました
# カスタマイズ用: burger-war-core:test
# 開発環境用　　: burger-war-dev:test
#--------------------------------------------------------------------
```

<br />

## 開発用のDockerコンテナの起動

Dockerイメージのビルドができたら、Dockerコンテナを起動しましょう。  
Dockerコンテナとして起動することで、Dockerイメージにインストールしたツールなどを使うことができます。

以下のコマンドでディレクトリを移動してから、以降の手順を実施して下さい。

```
cd ~/catkin_ws/src/burger_war_dev
```

<br />

### バージョンを指定せずにコンテナを起動
--------------------------------------------------------------------

以下のコマンドで、バージョンが`latest`のDockerイメージからDockerコンテナを起動します。

```
bash commands/docker-launch.sh
```

以下のメッセージが表示されれば、コンテナの起動は成功です。

```
#--------------------------------------------------------------------
# 開発用のコンテナを起動しました
# USE IMAGE NAME: burger-war-dev:latest
# CONTAINER NAME: burger-war-dev
#--------------------------------------------------------------------
```

試しに以下のコマンドで、開発用のDockerコンテナにインストールされたGazeboを起動してみましょう。

```
bash commands/kit.sh -c gazebo
```

以下のようなGazeboの画面が表示されれば成功です。  
右上の×ボタンからGazeboを終了して下さい。

※Gazeboの初回立ち上げには数分かかることもあります（その間、画面は黒いままです）


![gazebo起動](https://user-images.githubusercontent.com/76457573/105619906-8bb5e580-5e3a-11eb-8385-10eaa31e0133.png)


<br />

#### Gazeboが起動しない場合
--------------------------------------------------------------------
お使いのパソコンによっては、以下のようなエラーが表示されて、Gazeboが起動しないかもしれません。

その場合は、[カスタマイズしたDockerイメージの作成](#カスタマイズしたDockerイメージの作成)によって、お使いのパソコンに合ったドライバをインストールしたDockerイメージを作成して下さい。

```
libGL error: No matching fbConfigs or visuals found
libGL error: No matching fbConfigs or visuals found
libGL error: failed to load driver: swrast
libGL error: failed to load driver: swrast
X Error of failed request:  GLXBadContext
  X Error of failed request:  GLXBadContext
  Major oパソコンode of failed request:  152 (GLX)
Major oパソコンode of failed request:  152 (GLX)
  Minor oパソコンode of failed request:  6  Minor oパソコンode of failed request:  6 (X_GLXIsDirect) (X_GLXIsDirect)

    Serial number of failed request:  44Serial number of failed request:  44
  
  Current serial number in output stream:  43Current serial number in output stream:  43
```

<br />


### バージョンを指定してコンテナを起動
--------------------------------------------------------------------
バージョンを指定したDockerイメージからコンテナを起動する場合は、以下のコマンドを実行して下さい。

```
bash commands/docker-launch.sh -v test
```

起動する開発用のコンテナ名はどのバージョンのDockerイメージから作成しても、`burger-war-dev`となります。

もし、既に開発用のコンテナが起動中や作成済みだった場合は、既存のコンテナの停止と削除を自動で行い、`-v`で指定したバージョンのDockerイメージから新しいコンテナを作成・起動するようになっています。

<br />


## ワークスペースのビルド


```
bash commands/kit.sh -c catkin build
```

もし、catkin  buildコマンドに引数を渡したい場合は、以下のようにbuildの後に続けて渡して下さい。

```
bash commands/kit.sh -c catkin build -j8 -DCMAKE_CXX_FLAGS=-O0
```

コマンドの出力結果はcatkin buildの出力そのままになります。

<br />

## シミュレーションの実行

以下のコマンドで、シミュレータ､ロボット(turtle_bot)、審判サーバー､観戦画面が起動します。

```
bash commands/kit.sh -s sim_with_judge.sh
```

以下のようなフィールドが現れロボットが2台出現し、審判画面も表示されます。

![sim_with_judge](https://user-images.githubusercontent.com/76457573/105665129-aad77480-5f19-11eb-985c-49ac2f3bfb9e.png)

フィールドとロボットが立ち上がったら、別のターミナルで以下のマンドを実行して下さい。  
ロボットが動き出します。  

```
bash commands/kit.sh -s start.sh
```

敵プログラムはレベル１−３まで３種類用意しています。（デフォルトではレベル１）  
下記のように -l 引数によって変更できます。

level 2

```
bash commands/kit.sh -s start.sh -l 2
```

level 3

```
bash commands/kit.sh -s start.sh -l 3
```

<br />

### 審判サーバーを立ち上げずにシミュレータとロボットのみ立ち上げる場合
--------------------------------------------------------------------

```
bash commands/kit.sh roslaunch burger_war setup_sim.launch
```

フィールドとロボットが立ち上がったら、別のターミナルで以下のマンドを実行して下さい。

```
bash commands/kit.sh -s start.sh
```

審判サーバーが必要ない場合は直接launch ファイルを実行しても走行可能です。  
上記と同様にレベル設定も可能です。(defaunt 1)

```
bash commands/kit.sh roslaunch burger_war sim_robot_run.launch enemy_level:=1
```

<br />

## 起動したコンテナの中で操作をしたい場合

起動した開発用コンテナの中で何か操作をしたいことがあるかもしれません。

その場合は、以下のコマンドを実行して下さい。

```
bash commands/kit.sh 
```

以下のように開発用コンテナの中で対話モードでbashが起動します。

```
#--------------------------------------------------------------------
# 以下のコンテナでbashを起動します
# CONTAINER NAME: burger-war-dev
# EXEC COMMAND  : bash 
#--------------------------------------------------------------------
developer@hostname:~/catkin_ws$ 
```

対話的に起動する必要がない場合は、以下のように`-c`の後に実行したいコマンドを渡して下さい。

```
bash commands/kit.sh -c gazebo
```

## 短縮コマンドの設定例
Dockerコンテナの中でコマンドを実行する場合、以下のようにコマンドが長くなり入力が大変です。  
また、現在のディレクトリの位置にも配慮しなければなりません。

```
bash commands/kit.sh -s sim_with_judge.sh
```

そこで、エイリアスというbashの機能でコマンドの別名を`$HOME/.bashrc`に定義しておけば、実行が楽になります。

以下は設定例です。

```
# robocon aliases
kitsh=$HOME/catkin_ws/src/burger_war_dev/commands/kit.sh
alias kit="bash ${kitsh} $@"
alias kitc="bash ${kitsh} -c $@"
alias ws-build="bash ${kitsh} -c catkin build"
alias sim-launch="bash ${kitsh} -s sim_with_judge.sh"
alias sim-start="bash ${kitsh} -s start.sh"
```

`$HOME/.bashrc`を修正後、以下のコマンドで設定を反映させて下さい。  
(修正後に新しく起動したbashには自動で反映されます)

```
source ~/.bashrc
```

上記サンプルの設定後は、以下のように短いコマンドでそれぞれ実行できるようになります。

```
kit         # コンテナの中のbashを対話モードで起動
kitc        # コンテナの中の"bash -c 引数"でコマンドを実行(kitc envなど)
ws-build    # ワークスペースのビルド
sim-launch  # シミュレータの起動
sim-start   # シミュレーションの開始
```

エイリアスは、既存のコマンドと名前が被らないように注意して下さい。

<br />

## Dockerfileの構成について
Dockerfileの構成は以下のようになっています。

![Dockerfileの継承図](https://user-images.githubusercontent.com/76457573/105800339-d7eb5c00-5fd9-11eb-9890-9e426c6893c4.png)

参加者の方が修正するDockerfileは、黄色の「burger-war-core」と「burger-war-dev」になります。
他のファイルは修正しないで下さい。

<br />

## グラフィックボードのドライバの補足
Gazeboを起動しようとしたときに、以下のようなエラーメッセージが出てGazeboが起動しない場合、ドライバのインストールが必要です。

```
libGL error: No matching fbConfigs or visuals found
libGL error: failed to load driver: swrast
X Error of failed request:  GLXBadContext
  Major opcode of failed request:  152 (GLX)
  Minor opcode of failed request:  6 (X_GLXIsDirect)
  Serial number of failed request:  44
  Current serial number in output stream:  43
```

その場合は、以下の順番でGazeboが動くか試しながら、環境構築をされるのが良いでしょう。

1. ubuntu-driversによる自動インストールを試す
2. ホストPCのドライバを調べて、同じドライバをインストールを試す

ドライバのインストール方法は、お使いのグラフィックボードによって変わってきます。  
お使いのグラフィックボード用の手順を参考に、ドライバをインストールして下さい。

いずれの手順でも、Dockerfileの修正が終わったら、以下のDockerイメージを再作成し、Gazeboが起動するか確認して下さい。

```
bash commands/docker-build.sh
bash coomands/docker-launch.sh
bash commands/kit.sh -c gazebo
```

### ホストPCが利用中のドライバの確認方法
以下のコマンドで、使用しているホストPCがどのドライバを使っているか確認して下さい。

```
software-properties-gtk
```

表示されたウィンドウの「追加のドライバー」タブを選択すると、以下のように現在利用しているドライバが選択されている状態になっており、この例では「nvidia-driver-450」というパッケージのドライバを使用していることが分かります。  

![software-properties-gtk](https://user-images.githubusercontent.com/76457573/105653173-74d8c700-5efe-11eb-9d57-902ac7f79aa3.png)

### NVIDIAの場合
NVIDIAのドライバの場合、以下のいずれかの方法でインストールして下さい。

#### Ubuntuの標準バージョンのドライバのインストール
--------------------------------------------------------------------
`docker/dev/Dokcerfile`を以下の部分の行頭の#を削除して、`nvidia-driver-450`の部分を[ホストPCが利用中のドライバの確認方法](#ホストPCが利用中のドライバの確認方法)調べたドライバに書き換えて下さい。

```
# NVIDIAのドライバをインストールする例１) Ubuntのデフォルトバージョンをインストール
#-------------------------------------------------
RUN apt-get update -q && apt-get install -y \
    nvidia-driver-450 \
    && rm -rf /var/lib/apt/lists/* \
```

Dockerfileの修正が終わったら、Dockerイメージを再作成し、Gazeboが起動するか確認して下さい。

#### 詳細なバージョンを指定してインストール
--------------------------------------------------------------------
もし、[Ubuntuの標準バージョンのドライバのインストール)](#Ubuntuの標準バージョンのドライバのインストール)で動かない場合、ホストPCにインストールされているドライバのマイナーバージョンの違いが原因かもしれません。

以下のコマンドで詳細なバージョンを確認して下さい。

```
apt list --installed nvidia-driver-*                    # NVIDIAの場合
apt list --installed xserver-xorg-video-intel*          # Intel(内蔵)の場合
apt list --installed xserver-xorg-video-radeon*         # AMD/ATI(Radeon)の場合
```

例えば、以下のような出力になります。

```
一覧表示... 完了
nvidia-driver-440/bionic-updates,bionic-security,now 450.102.04-0ubuntu0.18.04.1 amd64 [インストール済み]
nvidia-driver-450/bionic-updates,bionic-security,now 450.102.04-0ubuntu0.18.04.1 amd64 [インストール済み、自動]
```

この例では、「450.102.04」というバージョンであることが分かります。


`docker/dev/Dokcerfile`の以下の箇所から行頭の#を削除して、`ARG DRIVER_VERSION=450.80.02`の部分を調べたバージョンに変更して下さい。

```
# NVIDIAのドライバをインストールする例２) バージョンを指定してインストール
# 参考：https://gitlab.com/nvidia/container-images/driver/-/blob/master/ubuntu18.04/Dockerfile
#-------------------------------------------------
ARG BASE_URL=https://us.download.nvidia.com/tesla
ARG DRIVER_VERSION=450.80.02
ENV DRIVER_VERSION=$DRIVER_VERSION

RUN cd /tmp && \
    curl -fSsl -O $BASE_URL/$DRIVER_VERSION/NVIDIA-Linux-x86_64-$DRIVER_VERSION.run && \
    sh NVIDIA-Linux-x86_64-$DRIVER_VERSION.run -x && \
    cd NVIDIA-Linux-x86_64-$DRIVER_VERSION* && \
    ./nvidia-installer --silent \
                       --no-kernel-module \
                       --install-compat32-libs \
                       --no-nouveau-check \
                       --no-nvidia-modprobe \
                       --no-rpms \
                       --no-backup \
                       --no-check-for-alternate-installs \
                       --no-libglx-indirect \
                       --no-install-libglvnd \
                       --x-prefix=/tmp/null \
                       --x-module-path=/tmp/null \
                       --x-library-path=/tmp/null \
                       --x-sysconfig-path=/tmp/null && \
    rm -rf /tmp/*
```

Dockerfileの修正が終わったら、Dockerイメージを再作成し、Gazeboが起動するか確認して下さい。

### Intelの場合
--------------------------------------------------------------------
追加のグラフィックボードがないPCの場合、Intelのデフォルトドライバで動くかと思います。  
ただし、Intel GPUのハードウェアアクセラレーションを有効にする場合は、追加でドライバをインストールします。  
(もし、追加のグラフィックボードがないIntel CPUのパソコンでGazeboが起動しない場合も、本手順を試してみて下さい)

`docker/dev/Dokcerfile`の以下の箇所から行頭の#を削除して下さい。

```
# Intel(VAAPI)のドライバをインストールする例
#-------------------------------------------------
RUN apt-get update -q && apt-get install -y \
    i965-va-driver \
    && rm -rf /var/lib/apt/lists/*
```

Dockerfileの修正が終わったら、Dockerイメージを再作成し、Gazeboが起動するか確認して下さい。


### AMD/ATIの場合
--------------------------------------------------------------------
AMD/ATIのグラフィックボードを載せている場合、標準でインストールされるオープンソース版のドライバで動く可能性が高いようです。  
※本リポジトリでは、AMD/ATIのグラフィックボード搭載環境での動作確認は実施できておりません

もしGazeboが起動しない場合は、[ホストPCが利用中のドライバの確認方法](#ホストPCが利用中のドライバの確認方法)の手順でホストPCのドライバを確認して、以下のサイトなどを参考にDockerfileでドライバをインストールして下さい。  

- [Nvidia以外のカードでVDPAUハードウェアビデオアクセラレーションサポートを有効にするにはどうすればよいですか？](https://qastack.jp/ubuntu/88847/how-do-i-enable-vdpau-hardware-video-acceleration-support-for-non-nvidia-cards)

- [Ubuntu 18.04にAMDグラフィックドライバーをインストールする方法](https://www.it-swarm-ja.tech/ja/drivers/ubuntu-1804%E3%81%ABamd%E3%82%B0%E3%83%A9%E3%83%95%E3%82%A3%E3%83%83%E3%82%AF%E3%83%89%E3%83%A9%E3%82%A4%E3%83%90%E3%83%BC%E3%82%92%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB%E3%81%99%E3%82%8B%E6%96%B9%E6%B3%95/998272373/)



### グラフィックスドライバ関連の参考サイト
--------------------------------------------------------------------

- [Ubuntuで最新のNVIDIA、AMD、またはIntelグラフィックスドライバを入手する方法](https://ja.compozi.com/1404-how-to-get-the-latest-nvidia-amd-or-intel-graphics-drivers-on-ubuntu)
- [Linux mint , ubuntu で Intel GPU によるVAAPI（ ハードウェアアクセラレーション ） を使用できるようにする](https://2sc380.hatenablog.com/entry/2019/01/20/223311#f-98f0f069)
- [Linuxデバイス・ハードウェア関連まとめ - Qiita](https://qiita.com/aosho235/items/079b37a9485041b96ed0)


## その他

### PROXYの設定について
--------------------------------------------------------------------

[TODO:PROXYの設定例を記載する]





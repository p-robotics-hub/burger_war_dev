# Startup Guide of burger_war 
burger_warの開発環境を構築する手順について説明します。

## 目次

<!-- TOC -->

- [1. Startup Guide of burger_war](#1-startup-guide-of-burger_war)
    - [1.1. 目次](#11-%E7%9B%AE%E6%AC%A1)
    - [1.2. インストール](#12-%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB)
        - [1.2.1. このリポジトリのクローン](#121-%E3%81%93%E3%81%AE%E3%83%AA%E3%83%9D%E3%82%B8%E3%83%88%E3%83%AA%E3%81%AE%E3%82%AF%E3%83%AD%E3%83%BC%E3%83%B3)
        - [1.2.2. Dockerのインストール](#122-docker%E3%81%AE%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB)
    - [1.3. 開発用のDockerイメージの作成](#13-%E9%96%8B%E7%99%BA%E7%94%A8%E3%81%AEdocker%E3%82%A4%E3%83%A1%E3%83%BC%E3%82%B8%E3%81%AE%E4%BD%9C%E6%88%90)
        - [1.3.1. デフォルトのDockerイメージの作成とコンテナ起動](#131-%E3%83%87%E3%83%95%E3%82%A9%E3%83%AB%E3%83%88%E3%81%AEdocker%E3%82%A4%E3%83%A1%E3%83%BC%E3%82%B8%E3%81%AE%E4%BD%9C%E6%88%90%E3%81%A8%E3%82%B3%E3%83%B3%E3%83%86%E3%83%8A%E8%B5%B7%E5%8B%95)
            - [1.3.1.1. 開発用のDockerイメージの作成](#1311-%E9%96%8B%E7%99%BA%E7%94%A8%E3%81%AEdocker%E3%82%A4%E3%83%A1%E3%83%BC%E3%82%B8%E3%81%AE%E4%BD%9C%E6%88%90)
            - [1.3.1.2. 開発用のDockerコンテナの起動](#1312-%E9%96%8B%E7%99%BA%E7%94%A8%E3%81%AEdocker%E3%82%B3%E3%83%B3%E3%83%86%E3%83%8A%E3%81%AE%E8%B5%B7%E5%8B%95)
            - [1.3.1.3. Gazeboが起動しない場合](#1313-gazebo%E3%81%8C%E8%B5%B7%E5%8B%95%E3%81%97%E3%81%AA%E3%81%84%E5%A0%B4%E5%90%88)
        - [1.3.2. カスタマイズしたDockerイメージの作成とコンテナ起動](#132-%E3%82%AB%E3%82%B9%E3%82%BF%E3%83%9E%E3%82%A4%E3%82%BA%E3%81%97%E3%81%9Fdocker%E3%82%A4%E3%83%A1%E3%83%BC%E3%82%B8%E3%81%AE%E4%BD%9C%E6%88%90%E3%81%A8%E3%82%B3%E3%83%B3%E3%83%86%E3%83%8A%E8%B5%B7%E5%8B%95)
            - [1.3.2.1. Dockerfileの修正例](#1321-dockerfile%E3%81%AE%E4%BF%AE%E6%AD%A3%E4%BE%8B)
    - [1.4. ワークスペースの作成とビルド](#14-%E3%83%AF%E3%83%BC%E3%82%AF%E3%82%B9%E3%83%9A%E3%83%BC%E3%82%B9%E3%81%AE%E4%BD%9C%E6%88%90%E3%81%A8%E3%83%93%E3%83%AB%E3%83%89)
        - [1.4.1. ワークスペースの作成（初期化）](#141-%E3%83%AF%E3%83%BC%E3%82%AF%E3%82%B9%E3%83%9A%E3%83%BC%E3%82%B9%E3%81%AE%E4%BD%9C%E6%88%90%E5%88%9D%E6%9C%9F%E5%8C%96)
        - [1.4.2. ワークスペースのビルド](#142-%E3%83%AF%E3%83%BC%E3%82%AF%E3%82%B9%E3%83%9A%E3%83%BC%E3%82%B9%E3%81%AE%E3%83%93%E3%83%AB%E3%83%89)
    - [1.5. シミュレーションの実行](#15-%E3%82%B7%E3%83%9F%E3%83%A5%E3%83%AC%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3%E3%81%AE%E5%AE%9F%E8%A1%8C)
        - [1.5.1. 審判サーバーを立ち上げずにシミュレータとロボットのみ立ち上げる場合](#151-%E5%AF%A9%E5%88%A4%E3%82%B5%E3%83%BC%E3%83%90%E3%83%BC%E3%82%92%E7%AB%8B%E3%81%A1%E4%B8%8A%E3%81%92%E3%81%9A%E3%81%AB%E3%82%B7%E3%83%9F%E3%83%A5%E3%83%AC%E3%83%BC%E3%82%BF%E3%81%A8%E3%83%AD%E3%83%9C%E3%83%83%E3%83%88%E3%81%AE%E3%81%BF%E7%AB%8B%E3%81%A1%E4%B8%8A%E3%81%92%E3%82%8B%E5%A0%B4%E5%90%88)
    - [1.6. 起動したコンテナの中で操作をしたい場合](#16-%E8%B5%B7%E5%8B%95%E3%81%97%E3%81%9F%E3%82%B3%E3%83%B3%E3%83%86%E3%83%8A%E3%81%AE%E4%B8%AD%E3%81%A7%E6%93%8D%E4%BD%9C%E3%82%92%E3%81%97%E3%81%9F%E3%81%84%E5%A0%B4%E5%90%88)
    - [1.7. 短縮コマンドの設定例](#17-%E7%9F%AD%E7%B8%AE%E3%82%B3%E3%83%9E%E3%83%B3%E3%83%89%E3%81%AE%E8%A8%AD%E5%AE%9A%E4%BE%8B)
    - [1.8. Dockerfileの構成について](#18-dockerfile%E3%81%AE%E6%A7%8B%E6%88%90%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6)
    - [1.9. グラフィックボードのドライバの補足](#19-%E3%82%B0%E3%83%A9%E3%83%95%E3%82%A3%E3%83%83%E3%82%AF%E3%83%9C%E3%83%BC%E3%83%89%E3%81%AE%E3%83%89%E3%83%A9%E3%82%A4%E3%83%90%E3%81%AE%E8%A3%9C%E8%B6%B3)
    - [1.10. その他](#110-%E3%81%9D%E3%81%AE%E4%BB%96)

<!-- /TOC -->


<br />

## インストール
burger_warの開発に必要なツールをインストールします。

### このリポジトリのクローン
--------------------------------------------------------------------
まずは、gitをインストールします。

```
sudo apt-get install -y git
```

次にワークスペースディレクトリを作成し、本リポジトリと開発ツール用のリポジトリをクローンします。

```
mkdir -p ~/catkin_ws/src && cd ~/catkin_ws/src
git clone https://github.com/p-robotics-hub/burger_war_dev
git clone https://github.com/p-robotics-hub/burger_war_kit
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

もし、CPUがARM32bitかARM64bitの環境にインストールする場合は、`amd64`の代わりに以下の引数を指定して下さい。

```
bash commands/docker-install.sh armhf       # ARM32bit環境の場合
bash commands/docker-install.sh arm64       # ARM64bit環境の場合
```

Ubuntu以外のLinuxディストリビューションの場合は、以下の公式の手順を参照して下さい。

- [dockerのインストール](https://docs.docker.com/engine/install/)
- [docker-composeのインストール](https://docs.docker.com/compose/install/)


インストール完了後、一度パソコンを再起動して下さい。


<br />

## 開発用のDockerイメージの作成

Dockerのインストールが終わったら、開発環境用のDockerイメージを作成します。

以下のコマンドでディレクトリを移動してから、以降の手順を実施して下さい。

```
cd ~/catkin_ws/src/burger_war_dev
```

### デフォルトのDockerイメージの作成とコンテナ起動
--------------------------------------------------------------------

#### 開発用のDockerイメージの作成
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

<br />

#### 開発用のDockerコンテナの起動
--------------------------------------------------------------------

Dockerイメージのビルドができたら、Dockerコンテナを起動しましょう。  
Dockerコンテナとして起動することで、Dockerイメージにインストールしたツールなどを使うことができます。

以下のコマンドで、開発用のDockerコンテナを起動します。

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
bash commands/ws-attach.sh -c gazebo
```

以下のようなGazeboの画面が表示されれば成功です。

[TODO:Gazeboの起動画面の画像を追加]

<br />

#### Gazeboが起動しない場合
--------------------------------------------------------------------
お使いのパソコンによっては、以下のようなエラーが表示されて、Gazeboが起動しないかもしれません。

その場合は、次節で説明するカスタマイズしたDockerイメージの作成方法によって、お使いのパソコンに合ったドライバをインストールしたDockerイメージの作成して下さい。

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

### カスタマイズしたDockerイメージの作成とコンテナ起動
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

[TODO:core/Dockerfileの記載例を追加]

<br />

##### ドライバをインストールする場合

[TODO:dev/Dockerfileの記載例を追加]

[TODO:参考サイトへの参照を追加]

<br />

##### バージョンを指定してDockerイメージを作成する

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

バージョンを指定したDockerイメージからコンテナを起動する場合は、以下のコマンドを実行して下さい。

```
bash commands/docker-launch.sh -v test
```

起動する開発用のコンテナ名はどのバージョンのDockerイメージから作成しても、`burger-war-dev`となります。

もし、既に開発用のコンテナが起動中や作成済みだった場合は、既存のコンテナの停止と削除を自動で行い、`-v`で指定したバージョンのDockerイメージから新しいコンテナを作成・起動するようになっています。

<br />

## ワークスペースの作成とビルド

### ワークスペースの作成（初期化）
--------------------------------------------------------------------

ROSワークスペースの初期化(catkin_init_workspace)と初回のビルド(catkin_make)を行います。

開発用のコンテナを起動した状態で、以下のコマンドを実行して下さい。

```
bash commands/ws-init.sh
```

成功すれば、以下のようなメッセージが表示されます。

```
#--------------------------------------------------------------------
# ワークスペースを以下に作成しました
# PATH(host)  : /home/username/catkin_ws
# PATH(docker): /home/developer/catkin_ws
#--------------------------------------------------------------------
```

もし、既にワークスペースが存在する場合は、以下のようなメッセージが表示されます。

```
/home/developer/catkin_ws/CMakeLists.txtが既に存在します。
削除して再度ワークスペースの初期化を行いますか？(yes/no): 
```

既存のワークスペースを削除して、新しくワークスペースを削除したい場合は`yes`を入力してEnterキーを押して下さい。  
このとき削除するのは、以下のファイルとディレクトリです。  
`~/catkin_ws/src/`配下の`burger_war_dev`と`burger_war_kit`は削除しません。

```
~/catkin_ws/.catkin_workspace
~/catkin_ws/src/CMakeLists.txt
~/catkin_ws/build
~/catkin_ws/devel
```

<br />

### ワークスペースのビルド
--------------------------------------------------------------------

ROSワークスペースのビルド(catkin_make)のみを行いたい場合は、以下のコマンドを実行して下さい。

```
bash commands/ws-build.sh
```

もし、catkin_makeコマンドに引数を渡したい場合は、`--`の後に引数を渡して下さい。

```
bash commands/ws-build.sh -- -j8 -DCMAKE_CXX_FLAGS=-O0
```

コマンドの出力結果はcatkin_makeの出力そのままですが、一番最初の行に以下のような実行したコマンドが出力されます。

```
+ catkin_make -j8 -DCMAKE_CXX_FLAGS=-O0
```

<br />

## シミュレーションの実行

以下のコマンドで、シミュレータ､ロボット(turtle_bot),審判サーバー､観戦画面が起動します。

```
bash commands/kit-exec.sh -s sim_with_judge.sh
```

以下のようなフィールドが現れロボットが2台出現し、審判画面も表示されます。

[TODO:シミュレータ起動画面を表示]

フィールドとロボットが立ち上がったら、別のターミナルで以下のマンドを実行して下さい。

```
bash commands/kit-exec.sh -s start.sh
```

敵プログラムはレベル１−３まで３種類用意しています。（デフォルトではレベル１）  
下記のように -l 引数によって変更できます。

level 2

```
bash commands/kit-exec.sh -s start.sh -l 2
```

level 3

```
bash commands/kit-exec.sh -s start.sh -l 3
```

<br />

### 審判サーバーを立ち上げずにシミュレータとロボットのみ立ち上げる場合
--------------------------------------------------------------------

```
bash commands/kit-exec.sh roslaunch burger_war setup_sim.launch
```

フィールドとロボットが立ち上がったら、別のターミナルで以下のマンドを実行して下さい。

```
bash commands/kit-exec.sh -s start.sh
```

審判サーバーが必要ない場合は直接launch ファイルを実行しても走行可能です。  
上記と同様にレベル設定も可能です。(defaunt 1)

```
bash commands/kit-exec.sh roslaunch burger_war sim_robot_run.launch enemy_level:=1
```

<br />

## 起動したコンテナの中で操作をしたい場合

起動した開発用コンテナの中で何か操作をしたいことがあるかもしれません。

その場合は、以下のコマンドを実行して下さい。

```
bash commands/ws-attach.sh 
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
bash commands/ws-attach.sh -c gazebo
```

## 短縮コマンドの設定例

[TODO:commands/*を実行するためのbashrcのalias設定例を追記]

<br />

## Dockerfileの構成について

[TODO:Dockerfileの継承図を追加する]

<br />


## グラフィックボードのドライバの補足

[TODO:各メーカー別の補足情報を記載する]


## その他





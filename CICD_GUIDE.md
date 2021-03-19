# CI/CD Guide (by GitHub Actions)
本ドキュメントでは、本リポジトリで使用可能なGitHub Actionsについて記載しています。

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**目次**

- [1. CI/CDについて](#1-cicd%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6)
- [2. GitHub Actionsについて](#2-github-actions%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6)
  - [2.1 GitHub Actionsとは](#21-github-actions%E3%81%A8%E3%81%AF)
  - [2.2 GitHub Actionsワークフローの基本構成](#22-github-actions%E3%83%AF%E3%83%BC%E3%82%AF%E3%83%95%E3%83%AD%E3%83%BC%E3%81%AE%E5%9F%BA%E6%9C%AC%E6%A7%8B%E6%88%90)
- [3. 本リポジトリのアクション](#3-%E6%9C%AC%E3%83%AA%E3%83%9D%E3%82%B8%E3%83%88%E3%83%AA%E3%81%AE%E3%82%A2%E3%82%AF%E3%82%B7%E3%83%A7%E3%83%B3)
- [4. ドキュメント(mdファイル)の目次更新](#4-%E3%83%89%E3%82%AD%E3%83%A5%E3%83%A1%E3%83%B3%E3%83%88md%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%81%AE%E7%9B%AE%E6%AC%A1%E6%9B%B4%E6%96%B0)
  - [4.1 対象ファイルを追加する場合](#41-%E5%AF%BE%E8%B1%A1%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%82%92%E8%BF%BD%E5%8A%A0%E3%81%99%E3%82%8B%E5%A0%B4%E5%90%88)
- [5 自動ビルド/テストとリリース](#5-%E8%87%AA%E5%8B%95%E3%83%93%E3%83%AB%E3%83%89%E3%83%86%E3%82%B9%E3%83%88%E3%81%A8%E3%83%AA%E3%83%AA%E3%83%BC%E3%82%B9)
  - [5.1 プッシュによる自動実行](#51-%E3%83%97%E3%83%83%E3%82%B7%E3%83%A5%E3%81%AB%E3%82%88%E3%82%8B%E8%87%AA%E5%8B%95%E5%AE%9F%E8%A1%8C)
  - [5.2 ブラウザからの手動実行方法](#52-%E3%83%96%E3%83%A9%E3%82%A6%E3%82%B6%E3%81%8B%E3%82%89%E3%81%AE%E6%89%8B%E5%8B%95%E5%AE%9F%E8%A1%8C%E6%96%B9%E6%B3%95)
  - [5.3 テスト結果とログファイル](#53-%E3%83%86%E3%82%B9%E3%83%88%E7%B5%90%E6%9E%9C%E3%81%A8%E3%83%AD%E3%82%B0%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB)
  - [5.4 自動ビルドとテストで行っている処理](#54-%E8%87%AA%E5%8B%95%E3%83%93%E3%83%AB%E3%83%89%E3%81%A8%E3%83%86%E3%82%B9%E3%83%88%E3%81%A7%E8%A1%8C%E3%81%A3%E3%81%A6%E3%81%84%E3%82%8B%E5%87%A6%E7%90%86)
  - [5.5 GitHub Actionsによるテスト環境](#55-github-actions%E3%81%AB%E3%82%88%E3%82%8B%E3%83%86%E3%82%B9%E3%83%88%E7%92%B0%E5%A2%83)
  - [5.6 GitHubからcatkinパッケージを追加する場合](#56-github%E3%81%8B%E3%82%89catkin%E3%83%91%E3%83%83%E3%82%B1%E3%83%BC%E3%82%B8%E3%82%92%E8%BF%BD%E5%8A%A0%E3%81%99%E3%82%8B%E5%A0%B4%E5%90%88)
  - [5.7 ビルドコマンドを変更したい場合](#57-%E3%83%93%E3%83%AB%E3%83%89%E3%82%B3%E3%83%9E%E3%83%B3%E3%83%89%E3%82%92%E5%A4%89%E6%9B%B4%E3%81%97%E3%81%9F%E3%81%84%E5%A0%B4%E5%90%88)
- [その他](#%E3%81%9D%E3%81%AE%E4%BB%96)
  - [A. GitHub Actionsドキュメントリンク集](#a-github-actions%E3%83%89%E3%82%AD%E3%83%A5%E3%83%A1%E3%83%B3%E3%83%88%E3%83%AA%E3%83%B3%E3%82%AF%E9%9B%86)
  - [B. ghcr.ioにプッシュするためのシークレット作成手順](#b-ghcrio%E3%81%AB%E3%83%97%E3%83%83%E3%82%B7%E3%83%A5%E3%81%99%E3%82%8B%E3%81%9F%E3%82%81%E3%81%AE%E3%82%B7%E3%83%BC%E3%82%AF%E3%83%AC%E3%83%83%E3%83%88%E4%BD%9C%E6%88%90%E6%89%8B%E9%A0%86)
  - [C. ghcr.ioにプッシュしたイメージの公開](#c-ghcrio%E3%81%AB%E3%83%97%E3%83%83%E3%82%B7%E3%83%A5%E3%81%97%E3%81%9F%E3%82%A4%E3%83%A1%E3%83%BC%E3%82%B8%E3%81%AE%E5%85%AC%E9%96%8B)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## 1. CI/CDについて
昨今のソフトウェア開発では、多機能/高機能で高品質かつ短納期という無理難題な要求に応えるため、開発サイクルの一部(ビルド、テスト、リリースなど)を自動化して継続的に行うCI/CDと呼ばれる手法がよく使われています。

CI(Continuous Integration)では、コードに対して静的解析ツールの実施したり、ビルド・テストを自動化して工数を短縮しつつ品質を維持します。  
CD(Continuous Delivery または Continuous Deployment)では、テストされたソフトを自動でリリース(例えばWebシステムなら本番運用環境に反映など)します。

CI/CDを実現するためのツールとしては、Jenkinsのようなオンプレミス型のツールと、GitHub Actionsのようなクラウド型のサービスがあります。

本リポジトリでは、GitHub Actionsを使って以下の処理を行うことができます。

  1. ドキュメント(mdファイル)の目次更新
  2. Dockerイメージ/ロボットプログラムのビルド
  3. Dockerコンテナによるシミュレーション実行
  4. Dockerイメージのghcr.ioへのプッシュ

<br />

## 2. GitHub Actionsについて
### 2.1 GitHub Actionsとは
------------------------------------------------------------------------------
GitHub Actionsとは、GitHubが提供するCI/CDサービスです。

GitHub Actionsで行う処理は、「ワークフロー」という単位で実行され、YMAL形式のファイル(`.github/workflows/*.yml`)に分けて記載します。

YAMLファイルでは、実行する処理をシェルスクリプトのように記述できるため自由度は高いです。  
これにより、リポジトリ内の任意のスクリプトファイルを実行することも可能です。

さらに、[マーケットプレイス](https://github.com/marketplace?type=actions)には、便利なアクションがたくさん公開されています。  
これらをプラグインのように利用することで、ワークフローの作成がとても楽になります。

ただし、Publicリポジトリでない場合、以下のページのように従量課金制になることに注意が必要です。

- [GitHub Actionsの支払いについて](https://docs.github.com/ja/github/setting-up-and-managing-billing-and-payments-on-github/about-billing-for-github-actions)

また、Publicリポジトリであっても、以下の使用制限があります。

- [使用制限、支払い、管理](https://docs.github.com/ja/actions/reference/usage-limits-billing-and-administration)

<br />

### 2.2 GitHub Actionsワークフローの基本構成
------------------------------------------------------------------------------
GitHub Actionsの１つのワークフローファイル(`.github/workflows/*.yml`)は、以下の要素から成っています。

- イベント      　... トリガとなるイベント (GitHubへのPushや時刻指定など)
- 環境変数定義　　... ワークフロー内で参照する環境変数定義
- ジョブ      　　... 1つのランナー(コンテナや仮想マシンのようなもの)で実行するステップの集まり
- ステップ        ... 1つ以上のアクションからなる処理の集まり
- アクション      ... 実際に実行する各コマンド。マーケットプレイスで公開されたアクションも指定可能

以下が、実際のワークフローのサンプルコードです。

```yml
# ワークフロー名(Webブラウザ上に表示される名前)
name: Workflow Name

# 実行トリガーイベントの指定
on:
  # GitHubへのプッシュイベント時
  push:
    # トリガ対象ブランチの指定
    branches: [ main ]

# ワークフロー内で利用できる環境変数を定義
env:
  SAMPLE_NAME: "Alice"

# 実行する処理
jobs:
  Sample-Job:
    name: Job Name
    runs-on: ubuntu-20.04
    steps:
      - name: Sample Step1
        run: |
          # 実行する処理を記載
          echo "Hello ${{ env.SAMPLE_NAME }}"
      - name: Sample Step2
        run: |
          # 1つのステップで実行する処理は複数記載可能
          date
          curl -s 'wttr.in/osaka?lang=ja&1'
```

<br />

アクションでの出力結果はブラウザから確認できます。  
例えば、サンプルコードの出力結果は以下のようになります。

![sample-workflow](https://user-images.githubusercontent.com/76457573/111557943-0fec6f80-87d1-11eb-8802-4065c2c3e1fa.png)

GitHub Actionsの詳細については、[公式ドキュメント](https://docs.github.com/ja/actions/learn-github-actions)を参照して下さい。

<br />

## 3. 本リポジトリのアクション
前述のように、本リポジトリでは、以下の処理を行うGitHub Actionsを用意しています。

1. ドキュメント(mdファイル)の目次更新
2. Dockerイメージ/ロボットプログラムのビルド
3. Dockerコンテナによるシミュレーション実行
4. Dockerイメージのghcr.io(Dockerイメージを公開するサービス)へのプッシュ

ワークフローファイルとしては、以下の2つに分けています。

- `.github/workflows/update_toc.yml`   ... ドキュメントの自動更新
- `.github/workflows/image-test.yml`   ... 自動ビルド/テスト/ghcr.ioへのプッシュ

以降では、各ワークフローについて説明します。

<br />

## 4. ドキュメント(mdファイル)の目次更新
[Startup Guide](STARTUP_GUIDE.md)と本ドキュメントの目次はGitHubにファイルをプッシュした際に自動で作成しています。

該当のワーフローは、`.github/workflows/update_toc.yml`に記載しています。

目次の更新には、以下のアクションを利用しています。

- [technote-space/toc-generator@v3](https://github.com/technote-space/toc-generator)


### 4.1 対象ファイルを追加する場合
------------------------------------------------------------------------------
まず最初に、Markdownファイルの目次を追加したい箇所に、以下のコードを追加して下さい。

```md
<!-- START doctoc -->
<!-- END doctoc -->
```

次に、`.github/workflows/update_toc.yml`にファイルの以下の`TARGET_PATHS`に、自動作成したいファイルをカンマ区切りで追記して下さい。

```yml
    steps:
      - name: TOC Generator
        uses: technote-space/toc-generator@v3
        with:
          # 目次を更新するファイル
          TARGET_PATHS: STARTUP_GUIDE.md,CICD_GUIDE.md
          # 目次を作成する最大階層レベル
          MAX_HEADER_LEVEL: 3
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          # 目次の見出し
          TOC_TITLE: '**目次**'
```

追記後、`.github/workflows/update_toc.yml`をプッシュすれば、追記したファイルの目次を自動で作成するようになります。

<br />

## 5 自動ビルド/テストとリリース
本リポジトリでは、GitHub Actions上でDockerイメージのビルドからシミュレーションによるテストまで実行するワークフローを用意しています。

実行方法としては、Dockerイメージに影響するファイルの変更をGitHubにプッシュした場合の自動実行と、ブラウザを操作して実行する方法があります。

### 5.1 プッシュによる自動実行
-------------------------------------------------------------------------------
以下のファイル以外の修正をGitHubにプッシュすると、自動でビルドとテストを実行します。

- 'commands/**'
- '.gitignore'
- 'LICENSE'
- '**.md'

<br />

### 5.2 ブラウザからの手動実行方法
-------------------------------------------------------------------------------
プッシュ以外に、ブラウザから以下のフォームで実行することができます。

「Dockerイメージのリリース」に「yes」を指定すれば、ghcr.ioにイメージをプッシュすることができます。  
※GitHubへのプッシュによる自動実行ではイメージのリリースは行いません

ただし、Dockerイメージをプッシュするには以下の手順を事前に実施して下さい。

[ghcr.ioにプッシュするためのシークレット作成手順](#-b-ghcrioにプッシュするためのシークレット作成手順)

また、プッシュしたDockerイメージを公開するには以下の操作を行って下さい。

[ghcr.ioにプッシュしたイメージの公開](#-c-ghcrioにプッシュしたイメージの公開)

<br />

### 5.3 テスト結果とログファイル
-------------------------------------------------------------------------------
自動テストは、自分のロボットが3分間で1点以上取得していれば試験はパスとしています。

3分間というのは実際の実行時間ではなく、Gazeboのシミュレーション時間になります。

テスト終了後、実行したGitHub ActionsのArtifactsからログファイルをダウンロードできます。

#### テスト結果
自動テスト時に自分のロボットが取得した点数は以下の手順で確認できます。

##### 1. Actionsタブ → Burger-War Image Build → 結果を確認したいワークフロー実行結果をクリック
![結果1](https://user-images.githubusercontent.com/76457573/111601826-16e9a100-8816-11eb-944a-4d0a51f560b2.png)

##### 2. build-testジョブをクリック
![結果2](https://user-images.githubusercontent.com/76457573/111601830-181ace00-8816-11eb-9180-b295c913a2cd.png)

##### 3. Test Docker Imageをクリック
![結果3](https://user-images.githubusercontent.com/76457573/111601832-181ace00-8816-11eb-84ea-f98ba2e5575a.png)

##### 4. ログの一番下までスクロール
以下のように、相手ロボット(青)と自分のロボット(赤)が取得した点数を確認することができます。  
以下の場合は、相手ロボットが1点、自分のロボットが5点とっていることが分かります。

![結果4](https://user-images.githubusercontent.com/76457573/111601834-18b36480-8816-11eb-9eef-5ff826e3a194.png)

<br />

#### ログファイル
実行したGitHub ActionsのArtifactsから自動テスト実行時のログファイルをダウンロードできます。

![devのログ出力](https://user-images.githubusercontent.com/76457573/110598025-a19e2080-81c4-11eb-88fd-c2c34e618c76.png)

ダウンロードしたログファイル(`test_log/test`ディレクトリ配下)の概要は以下になります。

|ログファイル|説明
|:-----------|:---
|gazebo/*|$HOME/.gazebo/logディレクトリ配下のファイル
|ros/*|$HOME/.ros/logディレクトリ配下のファイル
|judge/*|burger_war_kit/judge/logsディレクトリ配下のファイル
|screenshot/*|試験実行時の画面キャプチャ画像
|sim_with_test.log|burger_war_kit/scripts/sim_with_test.shの出力ログ
|start_script.log|burger_war_kit/scripts/start.sh or start_test.shの出力ログ
|judge_server_result.log|試験終了時に審判サーバから取得した情報(/warState)

<br />

### 5.4 自動ビルドとテストで行っている処理
-------------------------------------------------------------------------------
GitHub Actionsの自動テストで行っている主な処理は以下になります。

1. burger-war-core/sim/roboイメージのビルド (`docker build`)
2. burger-war-coreコンテナ起動 (`docker run`)
3. ロボコンプロジェクトのビルド (`catkin build`)
4. burger-war-coreのテスト (`scripts/sim_run_test.sh`)
5. burger-war-core/sim/roboイメージのプッシュ　※手動実行で指定時のみ (`docker push`)

実際の処理は`.github/workflows/image-test.yml`を参照して下さい。

<br />

### 5.5 GitHub Actionsによるテスト環境
-------------------------------------------------------------------------------
#### ローカル環境
以下、ローカルでの実行環境のイメージです。

![ローカル環境](https://user-images.githubusercontent.com/76457573/111599374-890cb680-8813-11eb-9d08-b42c1a9e886d.png)

<br />

ローカル環境では、コンテナ起動時にホストPCの`$HOME/catkin_ws`ディレクトリをマウントしています。

本リポジトリのファイルは、`$HOME/catkin_ws/src`ディレクトリ配下に配置するため、ホストPC上での変更は、起動中のコンテナにも反映されます。

それにより、burger_war_devディレクトリ配下のファイルを修正したときに、burger-war-devイメージを再ビルドしなくていいようになっています。

<br />

#### GitHub Actions環境
以下、GitHub Actionsでの実行環境のイメージです。

![テスト実施環境](https://user-images.githubusercontent.com/76457573/111746658-aef89080-88d1-11eb-937d-8b9863d8f9e1.png)

GitHub ActionsではGUIを表示するディスプレイがない為、`Xvfb`という仮想ディスプレイを使用しているという違いがあります。

burger_war_kitのソースコードついては、リポジトリから毎回チェックアウトを行います。  
※burger-war-kitイメージはghcr.ioにプッシュされているlatest版を利用します

もし、`catkin_ws/src/`以下にburger_war_kit/burger_war_dev以外のcatkinパッケージを追加する場合は、`.github/workflows/image-test.yml`に追記するようにして下さい。

具体的な手順は次節で説明します。

<br />

### 5.6 GitHubからcatkinパッケージを追加する場合
-------------------------------------------------------------------------------
`catkin_ws/src/`以下にburger_war_kit/burger_war_dev以外のcatkinパッケージを追加する場合は、`.github/workflows/image-test.yml`に以下のように追記して下さい。  
※追記場所は、burger_war_kit/burger_war_devをチェックアウトしている前後に追記して下さい

```yml
# 追加ライブラリのチェックアウト
- name: Checkout Library Repository
  uses: actions/checkout@v2
  with:
    repository: tysik/obstacle_detector
    path: catkin_ws/src/obstacle_detector
```

`repository`には、追加したいパッケージのGitHubリポジトリのパスを指定して下さい。

`path`には、チェックアウトしたディレクトリ名を指定して下さい。  
※親ディレクトリは`catkin_ws/src/`から変更しないように注意して下さい

<br />

### 5.7 ビルドコマンドを変更したい場合
-------------------------------------------------------------------------------
作成したロボットプログラムをビルドするコマンドは、デフォルトでは`catkin build`です。

もし変更したい場合は、`.github/workflows/image-test.yml`の以下の`catkin build`の部分を修正して下さい。

```yml
# ロボコンプロジェクトのビルド
- name: Build Robot Programs
  run: |
    docker exec -u developer -t ${{ env.IMAGE_NAME }} bash -l -c "catkin build"
```

<br />

## その他
### A. GitHub Actionsドキュメントリンク集
-------------------------------------------------------------------------------
はじめに読んでおいたほうが良い公式ドキュメントへのリンク集です。

1. GitHub Action入門
    - [GitHub Actions入門](https://docs.github.com/ja/actions/learn-github-actions/introduction-to-github-actions)： GitHub Actionsの概要・構成要素など
    - [GitHub Actions の重要な機能](https://docs.github.com/ja/actions/learn-github-actions/essential-features-of-github-actions)： 環境変数やArtifactsの利用方法など
      - [GitHub Actionsのワークフロー構文](https://docs.github.com/ja/actions/reference/workflow-syntax-for-github-actions)： ワークフローに使うYAMLの要素
      - [ワークフローをトリガーするイベント](https://docs.github.com/ja/actions/reference/events-that-trigger-workflows)： トリガイベントのリスト
      - [環境変数](https://docs.github.com/ja/actions/reference/environment-variables)： デフォルトの環境変数のリストなど
      - [ワークフロー データを成果物として保存する](https://docs.github.com/ja/actions/guides/storing-workflow-data-as-artifacts)： Artifactsの詳細
    - [アクションの検索とカスタマイズ](https://docs.github.com/ja/actions/learn-github-actions/finding-and-customizing-actions)： アクションの検索/使用/カスタマイズ方法など
    - [複雑なワークフローを管理する](https://docs.github.com/ja/actions/learn-github-actions/managing-complex-workflows)： 依存ジョブやビルドマトリックス、サービスコンテナの利用方法など
2. 業務で利用する場合
    - [利用規約](https://docs.github.com/ja/github/site-policy/github-terms-of-service)
    - [GitHub Actionsの支払いについて](https://docs.github.com/ja/github/setting-up-and-managing-billing-and-payments-on-github/about-billing-for-github-actions)： 利用料金など
    - [使用制限、支払い、管理](https://docs.github.com/ja/actions/reference/usage-limits-billing-and-administration)： 使用可能なジョブ数など
    - [JenkinsからGitHub Actionsへの移行](https://docs.github.com/ja/actions/learn-github-actions/migrating-from-jenkins-to-github-actions)： JenkinsとGitHub Actionsの比較
    - [ワークフローを Organization と共有する](https://docs.github.com/ja/actions/learn-github-actions/sharing-workflows-with-your-organization)： Organizationでのワークフローやシークレットなどの共有方法
    - [自分のランナーをホストする](https://docs.github.com/ja/actions/hosting-your-own-runners)： 独自のランナーの利用方法
    - [GitHub Actions のセキュリティ強化](https://docs.github.com/ja/actions/learn-github-actions/security-hardening-for-github-actions)： シークレットの利用方法やセキュリティ対策

<br />


### B. ghcr.ioにプッシュするためのシークレット作成手順
-------------------------------------------------------------------------------
自動テストにパスしたイメージをghcr.ioにプッシュするためにはログインする必要があります。

そのため、ユーザー名とパスワードの代わりに`Personal access token`が必要になります。

事前に各自のGitHubアカウントで`Personal access token`を作成し、それを各自のリポジトリのシークレットとして登録しておく必要があります。

以下の手順に従って、[こちらのページ](https://github.com/settings/tokens)から作成して下さい。

<br />

#### 1. Personal access tokens の Generate new tokenをクリック
![PAT作成手順2](https://user-images.githubusercontent.com/76457573/106542236-c4467500-6546-11eb-84e8-76071223a224.png)

<br />

#### 2. Select scopes で権限設定
少なくとも以下にチェックを入れて、ページ下部にある[Generate token]をクリックして下さい。

- write:packages
- read:packages
- delete:packages

![PAT作成手順3](https://user-images.githubusercontent.com/76457573/106542385-15566900-6547-11eb-9763-c89951b94f0d.png)

<br />

#### 3. 生成された Personal access token をコピー
生成された`Personal access token`(下の画像の黒塗り部分)をコピーして下さい。

![PAT作成手順4](https://user-images.githubusercontent.com/76457573/106542405-21dac180-6547-11eb-9db1-125b09e336cf.png)

<br />

#### 4. シークレットを追加
各リポジトリで「Settings」→「Secrets」→「New Repository secret」をクリックして下さい。

![シークレット1](https://user-images.githubusercontent.com/76457573/111585196-51494300-8802-11eb-9f83-e3ab802c618d.png)

以下の画面が表示されたら、Nameは`GHCR_PASSWORD`、Valueには先程コピーした`Personal access token`の値を入力して、`Add secret`をクリックしてシークレットを追加して下さい。

![シークレット2](https://user-images.githubusercontent.com/76457573/111585204-527a7000-8802-11eb-8577-e667e5428330.png)

同じように、Nameが`GHCR_USERNAME`、Valueは各自のアカウント名のシークレットを追加して下さい。

<br />


### C. ghcr.ioにプッシュしたイメージの公開
-------------------------------------------------------------------------------
ghcr.ioにプッシュしたイメージを誰でも利用できるようにするには、イメージを公開する必要があります。

以下にburger-war-roboイメージを公開する手順を示します。  
他に公開したいイメージがある場合は、同じ手順で公開して下さい。

#### 1. アカウントのトップ画面でPackagesをクリック → 公開するイメージをクリック

![公開1](https://user-images.githubusercontent.com/76457573/111590618-adfc2c00-8809-11eb-991b-3ea935115017.png)

<br />

#### 2. Packages Settingsをクリック

![公開2](https://user-images.githubusercontent.com/76457573/111590620-ae94c280-8809-11eb-8be9-969d9b18e09b.png)

<br />

#### 3. Change visibilityをクリック

![公開3](https://user-images.githubusercontent.com/76457573/111590623-af2d5900-8809-11eb-8cbb-a6f5446e0a35.png)

<br />

#### 4. Publicを選択 → 公開するイメージ名を入力 → 一番下のボタンをクリック

![公開4](https://user-images.githubusercontent.com/76457573/111590626-af2d5900-8809-11eb-9074-7436b22ce645.png)

<br />

上記手順後、以下のように「Private」の記載が消えていることを確認して下さい。

![公開5](https://user-images.githubusercontent.com/76457573/111591134-61652080-880a-11eb-9031-c4336e0efd39.png)

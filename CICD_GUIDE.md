# CI/CD Guide (by GitHub Actions)
本ドキュメントでは、本リポジトリで使用可能なGitHub Actionsについて記載しています。

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**目次**

- [1. CI/CDについて](#1-cicd%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6)
- [2. GitHub Actionsについて](#2-github-actions%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6)
- [3. 本リポジトリのアクション](#3-%E6%9C%AC%E3%83%AA%E3%83%9D%E3%82%B8%E3%83%88%E3%83%AA%E3%81%AE%E3%82%A2%E3%82%AF%E3%82%B7%E3%83%A7%E3%83%B3)
- [4. ドキュメント(mdファイル)の目次更新](#4-%E3%83%89%E3%82%AD%E3%83%A5%E3%83%A1%E3%83%B3%E3%83%88md%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%81%AE%E7%9B%AE%E6%AC%A1%E6%9B%B4%E6%96%B0)
  - [4.1 対象ファイルを追加する場合](#41-%E5%AF%BE%E8%B1%A1%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%82%92%E8%BF%BD%E5%8A%A0%E3%81%99%E3%82%8B%E5%A0%B4%E5%90%88)
- [5 自動ビルド/テストとリリース](#5-%E8%87%AA%E5%8B%95%E3%83%93%E3%83%AB%E3%83%89%E3%83%86%E3%82%B9%E3%83%88%E3%81%A8%E3%83%AA%E3%83%AA%E3%83%BC%E3%82%B9)
  - [5.1 自動ビルドとテストで行っている処理](#51-%E8%87%AA%E5%8B%95%E3%83%93%E3%83%AB%E3%83%89%E3%81%A8%E3%83%86%E3%82%B9%E3%83%88%E3%81%A7%E8%A1%8C%E3%81%A3%E3%81%A6%E3%81%84%E3%82%8B%E5%87%A6%E7%90%86)
  - [5.2 自動ビルドとテストの実行トリガ](#52-%E8%87%AA%E5%8B%95%E3%83%93%E3%83%AB%E3%83%89%E3%81%A8%E3%83%86%E3%82%B9%E3%83%88%E3%81%AE%E5%AE%9F%E8%A1%8C%E3%83%88%E3%83%AA%E3%82%AC)
  - [5.3 GitHub Actionsによるテスト環境](#53-github-actions%E3%81%AB%E3%82%88%E3%82%8B%E3%83%86%E3%82%B9%E3%83%88%E7%92%B0%E5%A2%83)
  - [5.4 判定方法とログファイル](#54-%E5%88%A4%E5%AE%9A%E6%96%B9%E6%B3%95%E3%81%A8%E3%83%AD%E3%82%B0%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB)
  - [5.5 ビルドコマンドを変更したい場合](#55-%E3%83%93%E3%83%AB%E3%83%89%E3%82%B3%E3%83%9E%E3%83%B3%E3%83%89%E3%82%92%E5%A4%89%E6%9B%B4%E3%81%97%E3%81%9F%E3%81%84%E5%A0%B4%E5%90%88)
- [その他](#%E3%81%9D%E3%81%AE%E4%BB%96)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## 1. CI/CDについて
昨今のソフトウェア開発では、多機能/高機能で高品質かつ短納期という無理難題な要求に応えるため、開発サイクル(ビルド、テスト、リリース)を自動化して継続的に行う、CI/CDと呼ばれる手法がよく使われています。

CI(Continuous Integration)では、コードに対して静的解析ツールの実施したり、ビルド・テストを自動化して品質を維持します。  
一方、CD(Continuous Delivery または Continuous Deployment)では、テストされたソフトを自動でリリース(例えばWebシステムなら本番運用環境に反映)します。

CI/CDを実現するためのツールとしては、Jenkinsのようなオンプレミス型のツールと、GitHub Actionsのようなクラウド型のサービスがあります。

本リポジトリでは、GitHub Actionsを使うことで、以下の処理を行うようにしています。

  1. ドキュメント(mdファイル)の目次更新
  2. Dockerイメージ/ロボットプログラムのビルド
  3. Dockerコンテナによるシミュレーション実行
  4. Dockerイメージのghcr.ioへのプッシュ

<br />

## 2. GitHub Actionsについて
GitHub Actionsとは、GitHubが提供するCI/CDツールです。

GitHub Actionsにプッシュしたコードに対して、以下のようなことが行なえます。

- FormatterやLinterをかける
- ビルドしてテストを行う
- テストにパスしたコードをバージョンを付けてリリース

実際にGitHub Actionsで行う処理は、「ワークフロー」と呼ばれ、YMAL形式のファイル(`.github/workflows/*.yml`)に分けて記載します。

YAMLファイルでは、実行する処理をシェルスクリプトのように記述できるため自由度は高いです。  
これにより、リポジトリ内の任意のスクリプトファイルを実行することも可能です。

さらに、[マーケットプレイス](https://github.com/marketplace?type=actions)には、便利なアクションが公開されています。
これらをプラグインのように活用することで、ワークフローの作成が楽になります。

とても便利なGitHub Actionsですが、利用目的はあくまでCI/CD用途でなければなりません。
それ以外の用途で利用すると、アカウントの凍結や削除されてしまう可能性もあります。

また、Publicなリポジトリでない場合、以下のページのように従量課金制となることに注意が必要です。

- [GitHub Actionsの支払いについて](https://docs.github.com/ja/github/setting-up-and-managing-billing-and-payments-on-github/about-billing-for-github-actions)

また、Publicであっても、以下の使用制限があります。

- [使用制限、支払い、管理](https://docs.github.com/ja/actions/reference/usage-limits-billing-and-administration)

<br />


## 3. 本リポジトリのアクション
前述のように、本リポジトリでは、以下の処理を行うGitHub Actionsを用意しています。

1. ドキュメント(mdファイル)の目次更新
2. Dockerイメージ/ロボットプログラムのビルド
3. Dockerコンテナによるシミュレーション実行
4. Dockerイメージのghcr.ioへのプッシュ

実際には、1〜3で1つのワークフロー、4単体で1つのワークフローに分けています。

- `.github/workflows/update_toc.yml`   ... ドキュメントの自動更新
- `.github/workflows/image-test.yml`   ... 自動ビルド/テスト/ghcr.ioへのプッシュ

以降では、各ワークフローについて説明します。

<br />

## 4. ドキュメント(mdファイル)の目次更新
Startup Guideと本ドキュメントの目次はGitHubにファイルをプッシュした際に自動で作成しています。

該当のワーフローは、`.github/workflows/update_toc.yml`に記載しています。

目次の更新には、以下のアクションを利用しています。

- [technote-space/toc-generator@v3](https://github.com/technote-space/toc-generator)


### 4.1 対象ファイルを追加する場合
------------------------------------------------------------------------------
まず、目次を自動作成したいMarkdownファイルの、目次を追加したい箇所に、以下のコードを追加して下さい。

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

### 5.1 自動ビルドとテストで行っている処理
-------------------------------------------------------------------------------
GitHub Actionsの自動テストで行っている主な処理は以下になります。

1. burger-war-core/sim/roboイメージのビルド (`docker build`)
2. 仮想ディスプレイの起動 (`Xvfb`)
3. burger-war-coreコンテナ起動 (`docker run`)
4. ロボコンプロジェクトのビルド (`catkin build`)
5. burger-war-kitのテスト (`scripts/sim_run_test.sh`)
6. テスト実行ログの保存 (`GitHub Artifact`)

実際の処理は`.github/workflows/image-test.yml`を参照して下さい。

<br />

### 5.2 自動ビルドとテストの実行トリガ
-------------------------------------------------------------------------------
以下のファイルの修正をGitHubにプッシュすると、自動ビルドとテストをGitHub Actions上で実行します。

- `docker/core/**`
- `docker/sim/**`
- `docker/robo/**`
- `burger_navigation/**`
- `burger_war_dev/**`
- `.github/workflows/image-test.yml`

自動ビルドとテストは、どのブランチへプッシュしても実行されます。

<br />

### 5.3 GitHub Actionsによるテスト環境
-------------------------------------------------------------------------------
#### ローカル環境
ローカル環境では、コンテナ起動時にホストPCの`$HOME/catkin_ws`ディレクトリをマウントしています。

本リポジトリのファイルは、`$HOME/catkin_ws/src`ディレクトリ配下に配置するため、ホストPC上での変更は、起動中のコンテナにも反映されます。

それにより、burger_war_devディレクトリ配下のファイルを修正したときに、burger-war-coreイメージを再ビルドする必要はありません。

ただし、`docker`ディレクトリ配下のファイルは、burger-war-kitイメージのビルド時に反映される為、再ビルドするようにして下さい。

<br />

#### GitHub Actions環境
GitHub Actions上では、コンテナ起動時のマウントポイントが`$HOME/catkin_ws/`から`$HOME/catkin_ws/src/burger_war_dev/`に変わります。

また、上記ディレクトリには以下のディレクトリのみコピーします。

- `burger_navigation/`
- `burger_war_dev/`

`burger_war_kit`については、latest版のburger-war-kitイメージ作成時に予め埋め込まれたソースコードを参照します。
 
その他、GitHub ActionsではGUIを表示するディスプレイがない為、`Xvfb`という仮想ディスプレイを使用しているという違いがあります。

<br />

### 5.4 判定方法とログファイル
-------------------------------------------------------------------------------
自動テストは、自分のロボットが3分間で1点以上取得していれば試験はパスとしています。

3分間というのは実際の実行時間ではなく、Gazeboのシミュレーション時間になります。

テスト終了後、実行したGitHub ActionsのArtifactsから自動テスト実行時のログファイルをダウンロードできます。

![devのログ出力](https://user-images.githubusercontent.com/76457573/110598025-a19e2080-81c4-11eb-88fd-c2c34e618c76.png)

<br />

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


### 5.5 ビルドコマンドを変更したい場合
-------------------------------------------------------------------------------
作成されたロボットプログラムをビルドするコマンドは、デフォルトでは`catkin build`です。

もし変更したい場合は、`.github/workflows/image-test.yml`の以下の`catkin build`の部分を修正して下さい。

```
# ロボコンプロジェクトのビルド
- name: Build Robot Programs
  run: |
    docker exec -u developer -t ${{ env.IMAGE_NAME }} bash -l -c "catkin build"
```

<br />

## その他

# CI/CD Guide (by GitHub Actions)
本ドキュメントでは、本リポジトリで使用可能なGitHub Actionsについて記載しています。

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [1. CI/CDについて](#1-cicd%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6)
- [2. GitHub Actionsについて](#2-github-actions%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6)
- [3. 本リポジトリのアクション](#3-%E6%9C%AC%E3%83%AA%E3%83%9D%E3%82%B8%E3%83%88%E3%83%AA%E3%81%AE%E3%82%A2%E3%82%AF%E3%82%B7%E3%83%A7%E3%83%B3)
  - [3.1 ドキュメント(mdファイル)の目次更新](#31-%E3%83%89%E3%82%AD%E3%83%A5%E3%83%A1%E3%83%B3%E3%83%88md%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%81%AE%E7%9B%AE%E6%AC%A1%E6%9B%B4%E6%96%B0)
  - [3.2 ビルドコマンドを変更したい場合](#32-%E3%83%93%E3%83%AB%E3%83%89%E3%82%B3%E3%83%9E%E3%83%B3%E3%83%89%E3%82%92%E5%A4%89%E6%9B%B4%E3%81%97%E3%81%9F%E3%81%84%E5%A0%B4%E5%90%88)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## 1. CI/CDについて
昨今のソフトウェア開発では、多機能/高機能で高品質かつ短納期という無理難題な要求に応えるため、開発サイクル(ビルド、テスト、リリース)を自動化して継続的に行う、CI/CDと呼ばれる手法がよく使われています。

CI(Continuous Integration/Continuous Deployment)とは、ビルドやテストを自動化した品質管理手法です。  
日本語では「継続的インテグレーション」と呼ばれます。

CD(Continuous Delivery または )とは、テストで品質が保証されたコードを自動でリリース(例えばWebシステムなら運用環境に反映)することです。  
日本語では「継続的デリバリー」または「継続的デプロイ」と呼ばれます。

本リポジトリでは、CI/CDツールであるGitHub Actionsを使うことで、以下の処理を行うことができます。

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

以降で、各ワークフローについて説明します。

<br />


### 3.1 ドキュメント(mdファイル)の目次更新
-------------------------------------------------------------------------------
Startup Guideと本ドキュメントの目次はGitHubにファイルをプッシュした際に自動で作成しています。

該当のワーフローは`.github/workflows/update_toc.yml`に記載しています。

目次の更新には、以下のアクションを利用しています。

- [technote-space/toc-generator@v3](https://github.com/technote-space/toc-generator)


#### 対象ファイルを追加する場合
まず、目次を自動更新したいMarkdownファイルの、目次を追加したい箇所に、以下のコードを追加して下さい。

```md
<!-- START doctoc -->
<!-- END doctoc -->
```

次に、`.github/workflows/update_toc.yml`にファイルの以下の`TARGET_PATHS`に、カンマ区切りで更新したいファイルを追記して下さい。

```yml
    steps:
      - name: TOC Generator
        uses: technote-space/toc-generator@v3
        with:
          # 目次を更新するファイル
          TARGET_PATHS: STARTUP_GUIDE.md
          # 目次を作成する最大階層レベル
          MAX_HEADER_LEVEL: 3
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```


<br />

### 3.2 ビルドコマンドを変更したい場合
-------------------------------------------------------------------------------



<br />

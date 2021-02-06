# gitの使い方

## とりあえずこれをやれ！

### リポジトリのクローン
github上のリポジトリ（プロジェクトファイルのかたまり）をローカルにコピーする

``` terminal
$ git clone https://github.com/EndoNrak/burger_war_dev
```

### いまローカルにあるブランチの確認
ローカルのブランチといまどのブランチにいるかを確認するコマンド

``` terminal
$ git branch
```

こんな感じの表示が出るはず
いまローカルにmainブランチしかなく、mainブランチにいる

``` terminal
* main
```

### ブランチの作成
ローカルのブランチを作成
作業のブランチを分けておくことで、同時進行で複数の開発を進められる（とくにチーム開発では必須）
いまいるmainブランチをもとにdocs(ドキュメント作成)ブランチを作成

``` terminal
$ git checkout -b docs
```

さきほどのgit branchで確認

``` terminal
$ git branch
```

### リモートのブランチをローカルに反映
git cloneしただけではdefaltのブランチ（今回はmainブランチ）だけがcloneされる
さっき作ったローカルのdocsブランチにリモートのdocsブランチを反映させる

``` terminal
$ git pull origin docs
```

エラーが出た時
gitのリモートリポジトリの設定を確認

``` terminal
$ git remote -v
```

こんな感じの結果がでる。記載されたurlが正しいかどうか確認しよう

``` terminal
origin  https://github.com/EndoNrak/burger_war_dev.git (fetch)
origin  https://github.com/EndoNrak/burger_war_dev.git (push)
```

正しくなかった場合は次のコマンドで設定を変更しよう
``` terminal
$ git remote set-url origin https://github.com/EndoNrak/burger_war_dev.git
```

これで解決できたはず！

### ファイルの変更
なんでもいいのでファイルに変更を加える
今回はdocsフォルダになにか好きなファイルを作成してみてください

### ファイル変更をコミット（変更の履歴を残す）
ファイルの変更を行い、その変更の履歴を残すことをコミットという
ある、固まったファイルの変更群を履歴にまとめて残すことで、未来の自分やチームメイトにどんな意図で変更したのかを分かるようにしておく
この辺の説明はちょっと難しい

``` terminal
$ git add .
$ git commit -m "docs: trial commit [自分の名前]"
```

うえのコマンドの""内はコミットメッセージといって、そのコミットの内容を端的に表すメッセージを残しておく。
他の人が見てわかるコミットメッセージを残しておこう


### ローカルのブランチをリモートにプッシュ（反映）
自分のコミットをリモートのリポジトリに反映させれば、大まかな流れは完結する

``` terminal
$ git push origin head
もしくは
$ git push origin docs
```

エラーが出た場合
githubリポジトリへのアクセス権限設定がない場合が多い
リポジトリの管理者に自分のgithubアカウントをコラボレーターに招待してもらい、編集権限を獲得しよう
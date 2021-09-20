---
title: "Hugo + GitHub Pagesでブログを始めた"
date: 2021-08-11T22:35:56+09:00
tags: ["Hugo", "GitHub Pages", "Blog"]
categories: ["Hugo"]
draft: false
---

[Zenn.dev](https://zenn.dev/)に書くほどでもない個人的なメモを残すために，[Hugo](https://gohugo.io/) + [GitHub Pages](https://docs.github.com/ja/pages)で静的サイトを構築しました．
<!--more-->

実は以前[Jekyll](http://jekyllrb-ja.github.io/)で静的サイトを構築したことがありましたが，Hugoの方が遥かに高速にビルドできるように感じました．

# 作り方

## 環境

- macOS 10.15.7

## Hugo

以下のコマンドで[Hugo](https://gohugo.io/)をインストールしました．

```
brew install hugo
```

`blog`というディレクトリを作成しました．

```
hugo new site blog
```

## Harbor

[https://github.com/matsuyoshi30/harbor](https://github.com/matsuyoshi30/harbor)がシンプルで素敵だったのので拝借しました．

```
cd themes
git submodule add https://github.com/matsuyoshi30/harbor.git harbor
```

公式の`config.toml`から少しだけ修正しました．

```
theme = "harbor"
baseurl = "https://kakeami.github.io/blog/"
title = "Amiblog"
paginate = 3
languageCode = "jp"
DefaultContentLanguage = "jp"
enableInlineShortcodes = true
footnoteReturnLinkContents = "^"
publishDir = "docs"

# Optional
# If you use googleAnalytics, you set top-level options in config.toml to the beginning of the config file like other top-level options.
googleAnalytics = "UA-XXXXXXXX-XX"
# and disqus too.
disqusShortName = "yourdisqusshortname"

[params.goatcounter]
  domain="stats.domain.com"

[params.matomo]
  domain="stats.domain.com"
  id="123"

[Author]
  name = "kakeami"

[outputs]
  section = ["JSON", "HTML"]

[[params.nav]]
  identifier = "about"
  name = "About"
  icon = "fas fa-user fa-lg"
  url = "/about/"
  weight = 3

[[params.nav]]
  identifier = "tags"
  name = "Tags"
  icon = "fas fa-tag fa-lg"
  url = "tags"
  weight = 3

[[params.nav]]
  identifier = "categories"
  name = "Category"
  icon = "fas fa-folder-open fa-lg"
  url = "categories"
  weight = 3

#[[params.nav]]
#  identifier = "search"
#  name = "Search"
#  icon = "fas fa-search fa-lg"
#  url = "search"
#  weight = 3

#[[params.nav]]
#  identifier = "archives"
#  name = "Archives"
#  icon = "fas fa-archive fa-lg"
#  url = "archives"
#  weight = 3

# copy paste this block and change for each social media to add how many ever social media
# acounts/links you want
[[params.social]]
  name="name of social media"
  url="link to social media"
  icon="A icon from https://fontawesome.com/"

[params.logo]
  url = "icon.png" # static/images/icon.png
  width = 50
  height = 50
  alt = "Logo"
```

当面は日本語で書きたかったので，`languageCode`等は`jp`にしました．

[Qiita, Hugo + GitHub Pages（独自ドメイン適応）でサイトを作成・公開する](https://qiita.com/ysdyt/items/a581277dd1312a0e83c3)
を参考に，`publishDir`は`"docs"`にしました．

`search`および`archives`は自分のデフォルト環境では意図通り動作しなかったため，一旦コメントアウトしておきました．

`kakeami.github.io`は別の用途に残して置きたかった（現時点でアイデアがあるわけではないけど）ため，`kakeami.github.io/blog/`を`baseurl`として指定しました．

## GitHub Pages

`blog`リポジトリを作成し，`Settings` > `Pages`から公開設定を行いました．
詳細は
[GitHub Docs, GitHub Pages サイトの公開元を設定する](https://docs.github.com/ja/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
を参照いただければと思います．

## デプロイ用スクリプト

毎回`hugo`とタイプするのが面倒だったので，`push`までまとめて実行する`publish.sh`を作りました．

```
#!/bin/sh

hugo
git add . -A
git commit -m "$1"
git push origin master
```

# 感想

以前[Jekyll](http://jekyllrb-ja.github.io/)で静的サイトを構築したことがありましたが，より高速にビルドできてとても快適です．

# 今後の課題

- タイトルのフォントサイズの調整
- 日本語全文検索
- アーカイブ

# 参考

- [Qiita, Hugo + GitHub Pages（独自ドメイン適応）でサイトを作成・公開する](https://qiita.com/ysdyt/items/a581277dd1312a0e83c3)
- [GitHub Docs, GitHub Pages サイトの公開元を設定する](https://docs.github.com/ja/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- [https://github.com/matsuyoshi30/harbor](https://github.com/matsuyoshi30/harbor)

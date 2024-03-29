# atom-bk-frame

本ライブラリは、atom1116 が作成した Web・モバイルのバックエンドアプリケーション開発のための機能を提供するライブラリです。  
以下の開発方針のもと開発を行いました。

- Python によるフルスクラッチでの開発
- WebAPI を開発するための基本的な機能の開発
- [WSGI](https://peps.python.org/pep-0333/)仕様に則った Web フレームワークの開発
- Django ライクな Web フレームワーク

## インストール

```
$ pip install git+https://github.com/Atom1116/atom-bk-frame
```

## 提供機能一覧

| 機能             | 内容                                                                                                                                   |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| URL ルーティング | リクエスト URL により適切にリクエストをコントローラへ振り分けるフレームワーク機能。                                                    |
| コントローラ     | GET/POST/PUT/DELETE の処理を定義し、URL ルーティングからのリクエストのメソッドに応じてレスポンスを返す機能を有するフレームワーク機能。 |
| データベース操作 | DB へアクセスし操作する処理をまとめた機能                                                                                              |
| ミドルウェア     | リクエストとレスポンスに処理を加えることができるフレームワーク機能。                                                                   |
| CORS             | 異なるオリジンへのアクセス権提供機能(CORS 対応)                                                                                        |
| 認証・認可       | アプリケーションの認証・認可処理を提供するフレームワーク機能。詳細は[こちら](#認証・認可)。                                            |

## サンプルアプリケーション

本ライブラリを使用したサンプルアプリを開発しました。使用方法について参考にしてください。

https://github.com/Atom1116/todo-scratch

## ライブラリドキュメント

https://atom1116.github.io/atom-bk-frame/

## Python バージョン

- Python:v3.9 以上

## サーバーインターフェース仕様

本ライブラリで開発できる Web アプリケーションは、以下の Web サーバインターフェースの仕様に則ります。

- [PEP 333 – Python Web Server Gateway Interface v1.0](https://peps.python.org/pep-0333/)

WSGI インターフェースの Web サーバにおいて動作可能です。動作検証は[Gunicorn](https://gunicorn.org/)を採用しました。

## イントロダクション

イントロダクションとして、「Hello World」を返す WebAPI の作成手順を記載します。

### フォルダ構成

ルート直下にアプリケーションソースファイルを格納するフォルダ(app)を作成します。

```
root
├── app
│   ├── settings.py
│   └── urls.py
│   └── controllers
│       └── hello_controller.py
└── wsgi.py
```

### wsgi.py

WSGI インターフェースである Web サーバーとの中継ファイルを作成します。

```
from atom_bk_frame.core.wsgi_app import WsgiApp
import os

# settings.pyの所在を記載
os.environ.setdefault('SETTINGS_PATH', 'app.settings')

# このappプロパティがWSGIサーバとのインタフェースとなる。WSGIサーバへの設定時にはこちらのappプロパティを参照するように設定する。
app = WsgiApp()
```

### settings.py

アプリケーションの設定を記載します。詳しくは[こちら](https://github.com/Atom1116/todo-scratch/blob/develop/todo_scratch/bk_app/settings.py)を参照。

```
# アプリケーションプロジェクト設定(必須)
# アプリケーションプロジェクトのパス設定
APP_PATH = 'app'

# urlルーティングファイルのファイル名
URLS_PATH = 'urls'
```

### urls.py

url パスとコントローラを紐づけます。

```
import typing as t
from atom_bk_frame.core.url_pattern import UrlPattern
from app.controllers.hello_controller import HelloController

# 正規表現でマッチするURLパスとコントローラクラスを紐づける。
urlpatterns: t.List[UrlPattern] = [
    UrlPattern(path='/$', controller=HelloController()),
]
```

### contorller

サーバからコールされたメソッドから呼び出された時に実行する処理を記載します。
GET メソッドから呼び出された時、「Hello World」を返します。

```
from atom_bk_frame.controller.controller import Controller
from atom_bk_frame.http.request import Request
from atom_bk_frame.http.response.response import Response


class HelloController(Controller):
    """「Hello World」を返すコントローラ
    """

    def get(self, request: Request, **kwargs) -> Response:
        # 'Hello World'をリクエストボディへ設定
        return Response('Hello World')

```

## 認証・認可機能

本ライブラリでは認証・認可の機能を提供します。使用できる機能の内容は下記の通りです。

- セッションを用いた認証
  - 認証したユーザごとにセッション ID を振り出し、管理します。
  - Cookie にセッション ID を設定します。
- 管理者・非管理者の認可
  - 管理者と非管理者によるアクセスできる API の制限が可能です。
- パスワードのハッシュ化

下記のミドルウェアを アプリケーションフォルダの settings.py へ設定することにより使用可能です。

```
"atom_bk_frame.middleware.session_middleware.SessionMiddleware"
```

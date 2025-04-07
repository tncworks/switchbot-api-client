# switchbot-api-client

SwitchBot APIを利用してSwitchBotデバイスを操作するためのPythonクライアントです。特にStreamDeckからシーリングライトProを操作することに焦点を当てています。

## 機能

- SwitchBot API v1.1の認証対応
- シーリングライトProの電源操作（オン/オフ/切り替え）
- シーリングライトProの明るさ調整
- シーリングライトProの色温度調整
- StreamDeckから簡単に実行可能なコマンドライン引数対応

## 前提条件

- Python 3.6以上
- SwitchBotアカウント
- SwitchBot開発者プラットフォームからのAPIトークンとシークレット
- SwitchBot シーリングライトPro
- StreamDeck（オプション、StreamDeckから操作する場合）

## インストール

1. このリポジトリをクローンします。

```bash
git clone https://github.com/yourusername/switchbot-api-client.git
cd switchbot-api-client
```

2. 必要なパッケージをインストールします。

```bash
pip install requests
```

3. パッケージをインストールします（開発モード）。

```bash
pip install -e .
```

## 設定

1. SwitchBot開発者プラットフォーム（https://developer.switch-bot.com/）からトークンとシークレットを取得します。

2. ホームディレクトリに `switchbot_config.json` ファイルを作成し、以下の内容を記述します。

```json
{
  "token": "YOUR_SWITCHBOT_TOKEN",
  "secret": "YOUR_SWITCHBOT_SECRET",
  "devices": {
    "リビング": "DEVICE_ID_FOR_LIVING_ROOM_LIGHT",
    "寝室": "DEVICE_ID_FOR_BEDROOM_LIGHT"
  }
}
```

3. デバイスIDを取得するには、以下のPythonスクリプトを実行します。

```python
from switchbot_streamdeck.switchbot import SwitchBotAPIClient

client = SwitchBotAPIClient()
devices = client.get_devices()
print(devices)

# デバイスIDを確認し、config.jsonの"devices"セクションに追加してください
```

## 使用方法

### コマンドラインから使用

#### 電源操作

```bash
# 電源をオン/オフ切り替え
python -m switchbot_streamdeck.actions.power "リビング"

# 電源をオンにする
python -m switchbot_streamdeck.actions.power "リビング" --action on

# 電源をオフにする
python -m switchbot_streamdeck.actions.power "リビング" --action off
```

#### 明るさ調整

```bash
# 明るさを50%に設定
python -m switchbot_streamdeck.actions.brightness "リビング" 50
```

#### 色温度調整

```bash
# 色温度を3500K（暖色系）に設定
python -m switchbot_streamdeck.actions.color_temp "リビング" 3500
```

### StreamDeckから使用

StreamDeckアプリケーションで、「システム」→「Open」アクションを設定し、以下のようなコマンドを設定してください。

#### Windows環境の場合

```
cmd.exe /c "python -m switchbot_streamdeck.actions.power リビング"
```

#### Linux/Mac環境の場合

```
python -m switchbot_streamdeck.actions.power リビング
```

同様に、明るさや色温度の調整用のボタンも設定できます。

## プロジェクト構成

```
switchbot_streamdeck/
├── config.py            # 設定ファイル管理
├── actions/
│   ├── __init__.py      # アクションモジュールの初期化
│   ├── brightness.py    # 明るさ調整用のアクション
│   ├── color_temp.py    # 色温度調整用のアクション
│   └── power.py         # 電源操作用のアクション
└── switchbot/
    ├── __init__.py      # SwitchBotモジュールの初期化
    ├── api_client.py    # SwitchBot API v1.1クライアント（認証含む）
    └── ceiling_light.py # シーリングライトPro制御用クラス
```

## カスタマイズ

このコードをベースに、以下のようなカスタマイズも可能です：

1. シーンの設定（複数のデバイスを同時に操作）
2. タイマーや特定の時間に実行するスケジュール機能
3. 他のSwitchBotデバイス（カーテン、エアコン、加湿器など）への対応
4. GUIインターフェースの追加

## 注意事項

- SwitchBot APIには、リクエスト制限（例：1日あたり10,000リクエスト）があるため、短時間に大量のリクエストを送信しないようにご注意ください。
- APIトークンとシークレットは機密情報ですので、設定ファイルを安全に管理してください。

## ライセンス

Apache License 2.0

import os
import json
import pathlib
from typing import Dict, Optional

class Config:
    """SwitchBot APIの設定を管理するクラス"""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        コンフィグを初期化
        
        Args:
            config_file: 設定ファイルのパス。指定しない場合はデフォルトのパスを使用
        """
        if config_file is None:
            # Windows環境のホームディレクトリにある設定ファイルを使用
            home = pathlib.Path.home()
            self.config_file = home / "switchbot_config.json"
        else:
            self.config_file = pathlib.Path(config_file)
        
        self.token: str = ""
        self.secret: str = ""
        self.devices: Dict[str, str] = {}
        
        self.load_config()
    
    def load_config(self) -> None:
        """設定ファイルから設定を読み込む"""
        if not self.config_file.exists():
            print(f"設定ファイルが存在しません: {self.config_file}")
            print("新しい設定ファイルを作成するには save_config() を実行してください")
            return
        
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
                
            self.token = config.get("token", "")
            self.secret = config.get("secret", "")
            self.devices = config.get("devices", {})
        except Exception as e:
            print(f"設定の読み込み中にエラーが発生しました: {e}")
    
    def save_config(self) -> None:
        """現在の設定を設定ファイルに保存する"""
        config = {
            "token": self.token,
            "secret": self.secret,
            "devices": self.devices
        }
        
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print(f"設定を保存しました: {self.config_file}")
        except Exception as e:
            print(f"設定の保存中にエラーが発生しました: {e}")
    
    def set_device(self, name: str, device_id: str) -> None:
        """
        デバイスIDを名前と関連付けて保存
        
        Args:
            name: デバイスの名前
            device_id: デバイスID
        """
        self.devices[name] = device_id
        
    def get_device_id(self, name: str) -> Optional[str]:
        """
        名前からデバイスIDを取得
        
        Args:
            name: デバイスの名前
            
        Returns:
            デバイスID、見つからない場合はNone
        """
        return self.devices.get(name)

# デフォルトのコンフィグインスタンス
default_config = Config()
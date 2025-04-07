import base64
import hashlib
import hmac
import json
import time
import uuid
from typing import Any, Dict, List, Optional, Union

import requests

from switchbot_streamdeck.config import Config, default_config

class SwitchBotAPIClient:
    """SwitchBot API v1.1クライアント"""
    
    BASE_URL = "https://api.switch-bot.com/v1.1"
    
    def __init__(self, config: Optional[Config] = None):
        """
        SwitchBot APIクライアントを初期化
        
        Args:
            config: 設定オブジェクト。指定しない場合はデフォルト設定を使用
        """
        self.config = config or default_config
        
    def _generate_headers(self) -> Dict[str, str]:
        """
        SwitchBot API v1.1の認証ヘッダーを生成
        
        Returns:
            認証情報を含むHTTPヘッダー辞書
        """
        token = self.config.token
        secret = self.config.secret
        
        if not token or not secret:
            raise ValueError("APIトークンとシークレットを設定してください")
        
        nonce = str(uuid.uuid4())
        t = str(int(time.time() * 1000))
        
        string_to_sign = f"{token}{t}{nonce}"
        
        signature = base64.b64encode(
            hmac.new(
                secret.encode('utf-8'),
                msg=string_to_sign.encode('utf-8'),
                digestmod=hashlib.sha256
            ).digest()
        ).decode('utf-8')
        
        return {
            "Authorization": token,
            "t": t,
            "sign": signature,
            "nonce": nonce,
            "Content-Type": "application/json"
        }
        
    def get_devices(self) -> Dict[str, Any]:
        """
        登録されているすべてのデバイスのリストを取得
        
        Returns:
            デバイスリストを含むレスポンス
        """
        url = f"{self.BASE_URL}/devices"
        headers = self._generate_headers()
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        return response.json()
    
    def get_device_status(self, device_id: str) -> Dict[str, Any]:
        """
        特定のデバイスのステータスを取得
        
        Args:
            device_id: デバイスID
            
        Returns:
            デバイスのステータス情報
        """
        url = f"{self.BASE_URL}/devices/{device_id}/status"
        headers = self._generate_headers()
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        return response.json()
    
    def control_device(self, device_id: str, command: str, parameter: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        デバイスを制御するコマンドを送信
        
        Args:
            device_id: デバイスID
            command: 実行するコマンド
            parameter: コマンドのパラメータ（オプション）
            
        Returns:
            API応答
        """
        url = f"{self.BASE_URL}/devices/{device_id}/commands"
        headers = self._generate_headers()
        
        data = {
            "command": command,
            "parameter": parameter or {}
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        
        return response.json()
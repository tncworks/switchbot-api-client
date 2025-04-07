from typing import Dict, Optional, Union, Any

from switchbot_streamdeck.config import Config, default_config
from switchbot_streamdeck.switchbot.api_client import SwitchBotAPIClient

class CeilingLightPro:
    """SwitchBotシーリングライトProを操作するためのクラス"""
    
    def __init__(self, device_id: Optional[str] = None, device_name: Optional[str] = None,
                 config: Optional[Config] = None):
        """
        シーリングライトProを初期化
        
        Args:
            device_id: デバイスID（直接指定する場合）
            device_name: デバイス名（設定ファイルから取得する場合）
            config: 設定オブジェクト（指定しない場合はデフォルト設定を使用）
        """
        self.config = config or default_config
        self.api_client = SwitchBotAPIClient(config)
        
        if device_id:
            self.device_id = device_id
        elif device_name:
            self.device_id = self.config.get_device_id(device_name)
            if not self.device_id:
                raise ValueError(f"デバイス名 '{device_name}' のIDが設定ファイルに見つかりません")
        else:
            raise ValueError("device_id または device_name を指定してください")
    
    def get_status(self) -> Dict[str, Any]:
        """
        現在のステータスを取得
        
        Returns:
            デバイスのステータス情報
        """
        response = self.api_client.get_device_status(self.device_id)
        return response
    
    def turn_on(self) -> Dict[str, Any]:
        """
        電源をオンにする
        
        Returns:
            API応答
        """
        return self.api_client.control_device(self.device_id, "turnOn")
    
    def turn_off(self) -> Dict[str, Any]:
        """
        電源をオフにする
        
        Returns:
            API応答
        """
        return self.api_client.control_device(self.device_id, "turnOff")
    
    def set_brightness(self, brightness: int) -> Dict[str, Any]:
        """
        明るさを設定
        
        Args:
            brightness: 明るさ（1-100）
            
        Returns:
            API応答
        """
        if not 1 <= brightness <= 100:
            raise ValueError("明るさは1から100の範囲で指定してください")
            
        return self.api_client.control_device(
            self.device_id, 
            "setBrightness", 
            {"brightness": brightness}
        )
    
    def set_color_temperature(self, temperature: int) -> Dict[str, Any]:
        """
        色温度を設定
        
        Args:
            temperature: 色温度（2700-6500K）
            
        Returns:
            API応答
        """
        if not 2700 <= temperature <= 6500:
            raise ValueError("色温度は2700Kから6500Kの範囲で指定してください")
            
        return self.api_client.control_device(
            self.device_id, 
            "setColorTemperature", 
            {"colorTemperature": temperature}
        )
    
    def toggle_power(self) -> Dict[str, Any]:
        """
        電源のオン/オフを切り替え
        
        Returns:
            API応答
        """
        status = self.get_status()
        if "body" in status and "power" in status["body"]:
            if status["body"]["power"] == "on":
                return self.turn_off()
            else:
                return self.turn_on()
        else:
            # ステータスが取得できない場合はとりあえずオンにする
            return self.turn_on()
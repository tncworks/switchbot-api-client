import argparse
import sys
from typing import Optional

from switchbot_streamdeck.switchbot import CeilingLightPro

def main(device_name: str, temperature: int) -> None:
    """
    シーリングライトProの色温度を設定
    
    Args:
        device_name: デバイス名（設定ファイルに登録されている名前）
        temperature: 色温度（2700-6500K）
    """
    try:
        if not 2700 <= temperature <= 6500:
            print("エラー: 色温度は2700Kから6500Kの範囲で指定してください")
            sys.exit(1)
            
        light = CeilingLightPro(device_name=device_name)
        response = light.set_color_temperature(temperature)
        
        if response.get("statusCode") == 100:
            print(f"シーリングライトProの色温度を {temperature}K に設定しました: {device_name}")
        else:
            print(f"エラー: {response.get('message', '不明なエラー')}")
            
    except Exception as e:
        print(f"エラー: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SwitchBot シーリングライトProの色温度調整")
    parser.add_argument("device_name", help="デバイス名（設定ファイルに登録されている名前）")
    parser.add_argument("temperature", type=int, help="色温度（2700-6500K）")
    
    args = parser.parse_args()
    main(args.device_name, args.temperature)
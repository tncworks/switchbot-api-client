import argparse
import sys
from typing import Optional

from switchbot_streamdeck.switchbot import CeilingLightPro

def main(device_name: str, brightness: int) -> None:
    """
    シーリングライトProの明るさを設定
    
    Args:
        device_name: デバイス名（設定ファイルに登録されている名前）
        brightness: 明るさ（1-100）
    """
    try:
        if not 1 <= brightness <= 100:
            print("エラー: 明るさは1から100の範囲で指定してください")
            sys.exit(1)
            
        light = CeilingLightPro(device_name=device_name)
        response = light.set_brightness(brightness)
        
        if response.get("statusCode") == 100:
            print(f"シーリングライトProの明るさを {brightness}% に設定しました: {device_name}")
        else:
            print(f"エラー: {response.get('message', '不明なエラー')}")
            
    except Exception as e:
        print(f"エラー: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SwitchBot シーリングライトProの明るさ調整")
    parser.add_argument("device_name", help="デバイス名（設定ファイルに登録されている名前）")
    parser.add_argument("brightness", type=int, help="明るさ（1-100）")
    
    args = parser.parse_args()
    main(args.device_name, args.brightness)
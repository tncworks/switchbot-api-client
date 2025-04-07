import argparse
import sys
from typing import Optional

from switchbot_streamdeck.switchbot import CeilingLightPro

def main(device_name: str, action: str = "toggle") -> None:
    """
    シーリングライトProの電源を操作
    
    Args:
        device_name: デバイス名（設定ファイルに登録されている名前）
        action: 実行するアクション（"on", "off", または "toggle"）
    """
    try:
        light = CeilingLightPro(device_name=device_name)
        
        if action == "on":
            response = light.turn_on()
            print(f"シーリングライトProをオンにしました: {device_name}")
        elif action == "off":
            response = light.turn_off()
            print(f"シーリングライトProをオフにしました: {device_name}")
        else:  # toggle
            response = light.toggle_power()
            print(f"シーリングライトProの電源を切り替えました: {device_name}")
            
        if response.get("statusCode") != 100:
            print(f"エラー: {response.get('message', '不明なエラー')}")
            
    except Exception as e:
        print(f"エラー: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SwitchBot シーリングライトProの電源制御")
    parser.add_argument("device_name", help="デバイス名（設定ファイルに登録されている名前）")
    parser.add_argument("--action", choices=["on", "off", "toggle"], default="toggle",
                        help="実行するアクション（オン、オフ、または切り替え）")
    
    args = parser.parse_args()
    main(args.device_name, args.action)
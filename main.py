import os
import requests
from dotenv import load_dotenv
from datetime import datetime

# 환경 변수 로드
load_dotenv()

class DustAlertApp:
    def __init__(self):
        self.api_key = os.getenv('DUST_API_KEY')
        self.endpoint = "http://apis.data.go.kr/B552584/UlfptcaAlarmInqireSvc/getUlfptcaAlarmInfo"
        
        if not self.api_key:
            raise ValueError("❌ 오류: .env 파일에 DUST_API_KEY가 설정되지 않았습니다.")

    def get_data(self, item_code="PM10"):
        """
        공공데이터 API로부터 경보 발령 현황을 가져옵니다.
        item_code: PM10 (미세먼지), PM25 (초미세먼지)
        """
        current_year = str(datetime.now().year)
        
        params = {
            'serviceKey': self.api_key,
            'returnType': 'json',
            'numOfRows': '100',
            'pageNo': '1',
            'year': current_year,
            'itemCode': item_code
        }

        try:
            response = requests.get(self.endpoint, params=params, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            items = result.get('response', {}).get('body', {}).get('items', [])
            return items

        except requests.exceptions.RequestException as e:
            print(f"📡 네트워크 오류 발생: {e}")
            return None
        except Exception as e:
            print(f"❗ 데이터 분석 중 오류 발생: {e}")
            return None

    def display(self, items):
        if not items:
            print(f"\n✅ {datetime.now().strftime('%Y-%m-%d %H:%M')} 현재 발령된 경보가 없습니다.")
            return

        print(f"\n{'='*65}")
        print(f"{'지역':<12} | {'구분':<8} | {'농도':<8} | {'발령시간'}")
        print(f"{'-'*65}")
        
        for item in items:
            district = item.get('districtName', '알수없음')
            move = item.get('moveName', '-')
            issue_gbn = item.get('issueGbn', '-')
            issue_val = item.get('issueVal', '-')
            issue_date = item.get('issueDate', '-')
            issue_time = item.get('issueTime', '-')
            
            print(f"{f'{district}({move})':<14} | {issue_gbn:<8} | {issue_val:<8} | {issue_date} {issue_time}")
        print(f"{'='*65}\n")

if __name__ == "__main__":
    app = DustAlertApp()
    
    print("🔍 미세먼지(PM10) 경보 현황을 조회합니다...")
    pm10_data = app.get_data("PM10")
    app.display(pm10_data)
    
    print("🔍 초미세먼지(PM25) 경보 현황을 조회합니다...")
    pm25_data = app.get_data("PM25")
    app.display(pm25_data)

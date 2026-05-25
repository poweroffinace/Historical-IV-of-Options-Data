from dhanhq import DhanLogin
from Dhan_Tradehull import Tradehull
import datetime, os, requests


dhan_login = DhanLogin("1111660429")
app_id = "562f1a9c"
app_secret = "a40916e5-6935-4328-adf2-27e333ec3f9a"

# Step 1: Generate Consent and Open Browser for Login
# consent_id = dhan_login.generate_login_session(app_id, app_secret)

token_id = 'c48cd8c1-1042-4293-aa06-39c6e943cc58'
dhan_creds = dhan_login.consume_token_id(token_id, app_id, app_secret)

client_id    = dhan_creds.get('dhanClientId')
access_token = dhan_creds.get('accessToken')


dhan_login = DhanLogin(dhan_creds.get('dhanClientId'))
user_info = dhan_login.user_profile(dhan_creds.get('accessToken'))
print(user_info)
input('Press ENTER to continue')

tsl          = Tradehull(client_id, access_token)

print("Login success")

def get_fno_symbols():
  url1 = 'https://www.nseindia.com'
  url2 = 'https://www.nseindia.com/api/underlying-information'


  session = requests.Session()
  headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
      'Accept': '*/*',
      'Accept-Language': 'en-US,en;q=0.9',
      'Accept-Encoding': 'gzip, deflate',
      'Connection': 'keep-alive',
      'Referer': 'https://www.nseindia.com',
      'sec-ch-ua-platform': '"Windows"',
      'Sec-Fetch-Site': 'same-origin',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Dest': 'empty',
  }
  res1 = session.get(url1, headers=headers)
  res2 = session.get(url2, headers=headers, cookies=res1.cookies.get_dict())

  fno_list =  list(filter(lambda symbol : symbol != "", list(map(lambda obj : obj.get("symbol", ""), res2.json().get("data", {}).get("UnderlyingList", [])))))

  return fno_list

watchlist = get_fno_symbols()

expiries     = ["2021-01-28" ,"2021-02-25" ,"2021-03-25" ,"2021-04-29" ,"2021-05-27" ,"2021-06-24" ,"2021-07-29" ,"2021-08-26" ,"2021-09-30" ,"2021-10-28" ,"2021-11-25" ,"2021-12-30" ,"2022-01-27" ,"2022-02-24" ,"2022-03-31" ,"2022-04-28" ,"2022-05-26" ,"2022-06-30" ,"2022-07-28" ,"2022-08-25" ,"2022-09-29" ,"2022-10-27" ,"2022-11-24" ,"2022-12-29" ,"2023-01-25" ,"2023-02-23" ,"2023-03-29" ,"2023-04-27" ,"2023-05-25" ,"2023-06-29" ,"2023-07-27" ,"2023-08-31" ,"2023-09-28" ,"2023-10-26" ,"2023-11-30" ,"2023-12-28" ,"2024-01-25" ,"2024-02-29" ,"2024-03-28" ,"2024-04-25" ,"2024-05-30" ,"2024-06-27" ,"2024-07-25" ,"2024-08-29" ,"2024-09-26" ,"2024-10-31" ,"2024-11-28" ,"2024-12-26" ,"2025-01-30" ,"2025-02-27" ,"2025-03-27" ,"2025-04-24" ,"2025-05-29" ,"2025-06-26" ,"2025-07-31" ,"2025-08-28" ,"2025-09-30" ,"2025-10-28" ,"2025-11-25" , "2026-01-27" ,"2026-02-24" ,"2026-03-30" , "2026-04-28" ,"2026-05-26" ]


for name in watchlist:
    for expiry in expiries:

        try:
            file_name = f"{name}_{expiry}.csv"
            dir       = f"Options data/{name}/ATM"
            path = f"{dir}/{file_name}"
            os.makedirs(dir, exist_ok=True)
            if os.path.exists(path):
                print(f"{file_name} already exists. Continue...")
                continue


            from_date = datetime.datetime.strptime(expiry, "%Y-%m-%d") - datetime.timedelta(days=30)
            from_date = from_date.strftime("%Y-%m-%d")
            data      = tsl.get_expired_option_data(tradingsymbol=name,exchange="NSE",interval=1,expiry_flag="MONTH",expiry_code=1,strike="ATM",option_type="CALL",from_date=from_date,to_date=expiry)
            if len(data) > 0 : 
                data.to_csv(f"{path}", index=False)
                print(f"{name} {expiry} : Download completed")
            else:
                # print(f"{name} {expiry} : Download failed")
                dummy =5 
                
        except Exception as e:
            print(f"{name} {expiry} : Error {e}")
            continue



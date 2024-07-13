import pyotp
from datetime import datetime, timedelta


def send_otp(requset):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)  # time base one time password
    otp = totp.now()
    requset.session['otp_secret_key'] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=1)
    requset.session['otp_valid_date'] = str(valid_date)

    print(f'your one time password is {otp}')

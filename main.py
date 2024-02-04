from flask import Flask, render_template, request, redirect, send_file
from rembg import remove 
import os
import random
from io import BytesIO
import pymysql.cursors
import random as r
import time
import playsound as ps
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import toml
from mail import name, passwd

app = Flask(__name__)   
  
db = pymysql.connect(host='localhost',
                             user='root',
                             password='1234',
                             db='lib',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


con = db.cursor()

logged = False
@app.route('/', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/check_account', methods=['POST'])
def check_acc():
    global logged
    global isim
    global sifre
    global k_id
    try:
        if request.method == 'POST':
            kullanici_isim = request.form.get('username')
            kullanici_sifre = request.form.get('password')

            con.execute('SELECT username, password, id FROM kullanıcı_bilgi WHERE username = %s', (kullanici_isim,))
            kimlikler = con.fetchall()
            db.commit()
            for kimlik in kimlikler:
                isim = kimlik['username']
                sifre = kimlik['password']
                k_id = kimlik['id']

        if kullanici_isim == isim and kullanici_sifre == sifre:
            logged = True
            return redirect('/anasayfa')
        else:
            return redirect('err_1')
    except:
        #! Hata
        return redirect('err_1')

    
    #? LOGIN işlemi burada sona eriyor.


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/create_account', methods=['POST'])
def create_acc():
    global yarat_id
    global yarat_email
    global yarat_isim
    global yarat_sifre
    global code
    global code_id
    if request.method == 'POST':
        try:
            global code
            global code_id
            yarat_isim = request.form.get('username')
            yarat_sifre = request.form.get('password')
            yarat_email = request.form.get('email')
            yarat_id = r.randint(0, 9999999)
            code = random.randint(0, 9999999)
            code_id = random.randint(0, 9999999)

            return redirect('/auth_mail')
        except:
            #! Hata
            return redirect('/err_2')
        
    #? REGISTER işlemi burada sona eriyor
        
    #? POSTA DOĞRULAMA KISMI
        
@app.route('/auth_mail', methods=['GET', 'POST'])
def auth_mail():
    global yarat_email
    global yarat_id
    global yarat_isim
    global yarat_sifre
    global code
    sender_email = name
    sender_password = passwd

    receiver_email = yarat_email

    subject = "rembgpy için posta doğrulama"
    body = """
<!DOCTYPE html>
<html lang="en">
<head>
    <style>
        body{
            background-color: white;
            justify-content: center;
            align-items: center;
        }
        .title{
            color: black;
            font-family: monospace;
            font-size: 32px;
        }
        .container{
            margin-left:35%;
            border-radius: 30px;
            height: 250px;
            width: 400px;
            background-color: #f8b500;
            text-align: center;
            align-items: center;
        }
        .num_container{
            background-color: black;
            border-radius: 30px;
            width: 50%;
            align-items: center;
            text-align: center;
            margin-left:25%;
            transition: background-color 0.3s ease-in-out;
        }
        .code{
            font-family: monospace;
            font-size: 48px;
            transition: color 0.3s ease-in-out;
            color: white
        }
        .num_container:hover{
            background-color:#f8b500;

        }
        .num_container:hover .code{
            color:black
        }
    </style>
</head>
<body>
    <div class="container">
        <p class="title">rembgpy posta doğrulama kodu:</p>
        <div class="num_container">
            <p class="code">"""+str(code)+"""</p>
        </div>
    </div>
</body>
</html>
"""

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "html"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)  # SMTP sunucu adresi ve port numarası
        server.starttls()  # Güvenli bağlantı kurma
        server.login(sender_email, sender_password)  # SMTP sunucusuna giriş yapma
        server.sendmail(sender_email, receiver_email, message.as_string())  # E-postayı gönderme
        print("E-posta başarıyla gönderildi!")
    except Exception as e:
        return redirect('/err_7')
    finally:
        if 'server' in locals():
            server.quit()  # SMTP sunucusu ile bağlantıyı sonlandırma
    return render_template('dogrula_mail.html')

@app.route('/auth_backend', methods = ['POST'])
def auth_backend():
    global code
    global code_id
    try:
        if request.method == 'POST':
            global code
            auth_code = request.form.get('auth_code')

            con.execute('INSERT INTO mail_codes VALUES(%s, %s, %s)', (code_id, yarat_email, code))
            db.commit()


            con.execute('SELECT code FROM mail_codes WHERE email = %s',(yarat_email))
            mails = con.fetchall()
            db.commit()
            for mail in mails:
                ac = mail['code']
            if str(auth_code) == str(ac):
                db.commit()
                return redirect('/reg_sonuc')
            else:
                return redirect('/err_8')
            
    except:
        return redirect('/err_2')
        
@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')


            
@app.route('/sifrem')
def sifrem():
    return render_template('sifrem.html')

@app.route('/anasayfa')
def index():
    global logged
    try:
        if logged == True:
            return render_template("anasayfa.html")   
        elif logged == False:
            #! Hata
            return redirect('/err_3')
        else:
            #! Hata
            return('Bilinmeyen hata')
    except:
        #! Hata
        return redirect('/err_4')

@app.route('/upload')
def upload():
    global logged
    if logged == True:
        return render_template('yukle.html')
    else:
        #! Hata
        return redirect('/err_3')
    

@app.route('/sifremi_unuttum')
def sifremi_unuttum():
    return render_template('forgot_password.html')

@app.route('/change_password', methods = ['POST'])
def sifre_degistir():
    global change_id
    global change_email
    if request.method == 'POST':
        try:
            change_id = request.form.get('ID')
            change_email = str(request.form.get('femail'))
            return redirect('/yeni_sifre')
        except:
            #! Hata
            return redirect('/err_5')
@app.route('/yeni_sifre')
def yeni_sifre():
    return render_template('sifrem.html')

@app.route('/change_backend', methods = ['POST'])
def auth():
    if request.method == 'POST':
        try:
            change_sifre = request.form.get('new_password')
            con.execute('UPDATE kullanıcı_bilgi SET password = %s WHERE id = %s AND email = %s', (change_sifre, change_id, change_email))
            db.commit()
            return redirect('/sifirlandi')
        except:
            #! Hata
            return redirect('/err_5')
    
@app.route('/sifirlandi')
def sifirlandi():
    return render_template('sifirlandi.html')

@app.route('/basarili', methods=['POST'])
def basarili():
    if request.method == 'POST':

        file = request.files['file']
        input_data = file.read()
        output_data = remove(input_data)
        fname = random.randint(0, 9999999)
        output_path = str(fname)+'.png'

        return send_file(BytesIO(output_data), download_name=output_path)
        
            



@app.route('/reg_sonuc')
def reg_sonuc():
    global yarat_id
    global yarat_isim
    global yarat_sifre
    global yarat_email
    con.execute('INSERT INTO kullanıcı_bilgi VALUES(%s, %s, %s, %s)',(yarat_id, yarat_isim, yarat_sifre, yarat_email))
    return render_template('reg_sonuc.html', kayıt_id = yarat_id)

@app.route('/my_account')
def my_account():
    return render_template('hesabım.html', isim=isim, k_id = k_id)

  
#? ERROR (HATA) KISIMLARI

@app.route('/err_1')
def err_1():
    return render_template('err_1.html')

@app.route('/err_2')
def err_2():
    return render_template('err_2.html')

@app.route('/err_3')
def err_3():
    return render_template('err_3.html')

@app.route('/err_4')
def err_4():
    return render_template('err_4.html')

@app.route('/err_5')
def err_5():
    return render_template('err_5.html')

@app.route('/err_6')
def err_6():
    return render_template('err_6.html')

@app.route('/err_7')
def err_7():
    return render_template('err_7.html')

@app.route('/err_8')
def err_8():
    return render_template('err_8.html')

if __name__ == '__main__':  
    app.run(debug=True) 


#* By Alper Tuna KILIÇ
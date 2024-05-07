from flask import Flask, request
import boto3
import os
import datetime
import configparser
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:5173"]}})


# 設定ファイルのパス
config_file_path = 'config.ini'

# 設定ファイルを読み込む
config = configparser.ConfigParser()
config.read(config_file_path)

# AWSの認証情報
# AWSの秘密情報を取得する
aws_access_key_id = config['aws']['aws_access_key_id']
aws_secret_access_key = config['aws']['aws_secret_access_key']
aws_region_name = config['aws']['aws_region_name']
s3_bucket_name = config['aws']['s3_bucket_name']
endpoint_url = config['aws']['endpoint_url']

# S3クライアントの作成
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        endpoint_url = endpoint_url,
                        region_name=aws_region_name)

# ファイルをS3にアップロードするエンドポイント
@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    # POSTリクエストからファイルと位置情報を取得
    photo = request.files['photo']
    latitude = request.form['latitude']
    longitude = request.form['longitude']

    # ファイル名に位置情報と日時を含める
    timestamp = datetime.datetime.now().isoformat()
    filename = f"{timestamp}_{latitude}_{longitude}_{photo.filename}"

    # ファイルを一時保存
    temp_file_path = f"/tmp/{filename}"
    photo.save(temp_file_path)

    # S3にファイルをアップロード
    s3.upload_file(temp_file_path, s3_bucket_name, filename)

    # 一時保存したファイルを削除
    os.remove(temp_file_path)

    return {'message': 'Photo uploaded and location saved successfully'}

if __name__ == '__main__':
    app.run(debug=True)

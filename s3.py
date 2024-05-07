from flask import Flask, jsonify
import boto3

app = Flask(__name__)
# S3クライアントを作成
s3 = boto3.client(
    's3',
    aws_access_key_id='KP872A5Z7W2TYEVE9PN4',
    aws_secret_access_key='MAYXMl4sfjMsHXs9qCsHPKnZP/mTESYuPeUTwm8S',
    endpoint_url='https://s3.isk01.sakurastorage.jp',
    region_name='jp-north-1'
)
bucket_name = 'setouchi-test1'

print('s3.py')

@app.route('/list-objects', methods=['GET'])
def list_objects():
    response = s3.list_objects_v2(Bucket=bucket_name)
    objects = response.get('Contents', [])
    file_names = [obj['Key'] for obj in objects]
    return jsonify(file_names)

if __name__ == '__main__':
    app.run(debug=True, port=5173)

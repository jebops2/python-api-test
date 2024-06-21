# access_keys.py
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
KST = timezone(timedelta(hours=9))

## Boto3 활용한 AWS IAM 클라이언트 생성
iam = boto3.client(
    'iam',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='ap-northeast-2'
)

def list_access_keys_by_time(hours=None):
    access_keys_info = []
    try:
        # 모든 IAM User 리스트 조회
        paginator = iam.get_paginator('list_users')
        for page in paginator.paginate():
            for user in page['Users']:
                user_name = user['UserName']

                # 사용자별 Access Key와 기타 정보 확인
                response = iam.list_access_keys(UserName=user_name)
                if 'AccessKeyMetadata' in response:
                    for access_key in response['AccessKeyMetadata']:
                        create_date = access_key['CreateDate']
                        if hours is not None:
                            current_time = datetime.now(KST)
                            create_date_kst = create_date.astimezone(KST)
                            time_difference = current_time - create_date_kst

                            # 사용자가 입력한 Hours 를 초과한 값만 List에 추가
                            if time_difference > timedelta(hours=hours):
                                key_info = {
                                    'AccessKeyId': access_key['AccessKeyId'],
                                    'UserName': user_name,
                                    'Status': access_key['Status'],
                                    'CreateDate': create_date_kst.strftime('%Y-%m-%d %H:%M:%S')
                                }
                                access_keys_info.append(key_info)
                        else:
                            key_info = {
                                'AccessKeyId': access_key['AccessKeyId'],
                                'UserName': user_name,
                                'Status': access_key['Status'],
                                'CreateDate': create_date.astimezone(KST).strftime('%Y-%m-%d %H:%M:%S')
                            }
                            access_keys_info.append(key_info)
                else:
                    print(f"No access keys found for user {user_name}")

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error retrieving access keys: {e}")

    return access_keys_info

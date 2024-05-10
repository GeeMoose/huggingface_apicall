import boto3
from botocore.exceptions import NoCredentialsError

from dotenv import load_dotenv
import os
# 获取当前文件的目录
from pathlib import Path

# .env 文件的路径
env_path = '.env'
load_dotenv(env_path)

ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

region_name = os.getenv('REGION_NAME')
bucket = os.getenv('BUCKET')
cloudfront = os.getenv('CLOUDFRONT')

# 获取同级env环境变量文件

s3_client = boto3.client('s3', region_name=region_name, aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)

async def upload_image_file_to_s3(file_name, object_name):
    """
    Upload the image file to an S3 bucket and return the file URL
    """
    try:
        file_extension = object_name.lower().rsplit('.', 1)[-1]
        # 根据文件扩展名设置 ContentType
        if file_extension in ['jpg', 'jpeg', 'png', 'svg', 'webp']:
            content_type = "image/" + file_extension
        else:
            content_type = 'binary/octet-stream'  # 默认类型
        s3_client.upload_file(file_name, bucket, object_name, ExtraArgs={
            'ContentType': content_type
        })

        url = f"https://{cloudfront}/{object_name}"
        return url

    except NoCredentialsError:
        print("Credentials not available")
        return None
    except Exception as e:
        print(e)
        return None



#url = upload__to_s3_and_get_url(
#    '/Users/yuxh-mac/Desktop/work/openSource/speedpainter/outputs/line_art_123456789.png', bucket, 'line_art_123456789asdda')
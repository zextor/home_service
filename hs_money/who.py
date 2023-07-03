import io
import time
import picamera

# 카메라 객체 생성
camera = picamera.PiCamera()

# 해상도 설정
camera.resolution = (640, 480)

# 사진을 찍고 스냅샷을 메모리 변수에 저장
stream = io.BytesIO()
camera.capture(stream, format='jpeg')
stream.seek(0)
'''
datetime.datetime.now().strftime('%A')
'''

# 파일로 저장
with open('snapshot.jpg', 'wb') as file:
    file.write(stream.read())
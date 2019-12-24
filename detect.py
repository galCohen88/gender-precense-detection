import boto3 as boto3
import cv2


image_name = 'tmp.png'


def take_picture(img_name):
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    cv2.imwrite(img_name, frame)
    print("{} written!".format(img_name))
    cam.release()
    cv2.destroyAllWindows()


while True:
    take_picture(image_name)
    with open(image_name, 'rb') as f: # open the file in read binary mode
        data = f.read()

    client = boto3.client('rekognition', aws_access_key_id=access_key, aws_secret_access_key=secrete_key)

    print('detecting')

    response = client.detect_faces(
        Image={
            'Bytes': data
        },
        Attributes=['ALL']
    )
    img = cv2.imread(image_name)

    male = 0
    female = 0

    for face in response.get('FaceDetails'):
        width = face.get('BoundingBox').get('Width')
        height = face.get('BoundingBox').get('Height')
        left = face.get('BoundingBox').get('Left')
        top = face.get('BoundingBox').get('Top')
        gender = face.get('Gender').get('Value')

        im_height, im_width, channels = img.shape

        face_width = int(width * im_width)
        face_height = int(height * im_height)
        face_left_position = int(left * im_width)
        face_top_position = int(top * im_height)

        if gender == 'Male':
            male += 1
            color = (250, 206, 135)
        else:
            female +=1
            color = (147, 112, 219)
        img = cv2.rectangle(img, (face_left_position, face_top_position), (face_left_position+face_width, face_height+face_top_position), color, 5)

    female_percentage = (female / float(male+female)) * 100
    male_percentage = (male / float(male+female)) * 100

    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10, 700)
    fontScale = 1
    fontColor = (255, 0, 0)
    lineType = 2

    cv2.putText(img, 'Male percentage ' + str(int(male_percentage)) + ' Female percentage: ' + str(int(female_percentage)),
                bottomLeftCornerOfText,
                font,
                fontScale,
                fontColor,
                lineType)
    cv2.imshow("window", img)
    cv2.moveWindow('window', 200, 200)
    cv2.waitKey(1)



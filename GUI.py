#Required imports
import tensorflow as tf
import tensorflow.keras as keras
import numpy as np
import cv2

#Loading keras model 
model = tf.keras.models.load_model('keras_model.h5')

#initialization
img = np.ones([450,750],dtype ='uint8')*255
img[50:350,50:350]=0
wname = 'Canvas'
drawing = False
Valid_drawing = False
penThickness=17
cv2.namedWindow(wname)
percentage = np.array([0 for x in range(10)]).reshape((1,10))
cv2.putText(img,"1.Use \"Q\" to quit.",(50,370),fontFace = 1,fontScale =1,color = 0, thickness = 1)
cv2.putText(img,"2.Use \"C\" to clear the board.",(50,400),fontFace = 1,fontScale =1,color = 0, thickness = 1)
cv2.putText(img,"3.Use \"+\" or \"-\" to adjust marker size.",(50,430),fontFace = 1,fontScale =1,color = 0, thickness = 1)
    
def line_drawing(event,x,y,flags,param):
    global pt1_x,pt1_y,drawing,penThickness
    if event==cv2.EVENT_LBUTTONDOWN:
        drawing=True
        pt1_x,pt1_y=x,y
    elif event==cv2.EVENT_MOUSEMOVE:
        if drawing==True:
            cv2.line(img,(pt1_x,pt1_y),(x,y),color=255,thickness=penThickness)
            pt1_x,pt1_y=x,y
    elif event==cv2.EVENT_LBUTTONUP:
        drawing=False
        cv2.line(img,(pt1_x,pt1_y),(x,y),color=255,thickness=penThickness)


def update_percentage():
    img[50:350,400:700] = 255
    global percentage
    for i in range(10):
        cv2.putText(img,str(i),(360,75+30*i),fontFace = 1,fontScale =2,color = 0, thickness = 1)
        cv2.rectangle(img,(400,55+30*i),(700,75+30*i),128,1)
        img[55+30*i:75+30*i,400:401+int(300*(percentage[0][i]))] = 128

cv2.setMouseCallback(wname,line_drawing)  # line_drawing is a sub method called in the setMouseCallback method
while True:
    update_percentage()
    cv2.imshow(wname,img)
    key = cv2.waitKey(5)
    if key == ord('q'):
        break
    elif key ==ord('i'):
        instructions()
    elif key== ord("+") and penThickness<30:
        penThickness+=1
    elif key== ord("-") and penThickness>3:
        penThickness+=-1
    elif key == ord('c'):
        img[50:350,50:350]=0
    test = img[50:350,50:350]
    test = cv2.blur(test,(3,3))
    test = np.array(cv2.resize(test,(28,28),interpolation = cv2.INTER_LINEAR))
    test = np.reshape(test,(1,28,28))
    percentage = model.predict(test)

    
cv2.destroyAllWindows()



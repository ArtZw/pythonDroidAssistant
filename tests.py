import cv2
import HaarDetector as Detector
import sqlite3

conn = sqlite3.connect('db_test') #connect db
cursor = conn.cursor();
refPt = []
cropping = False
image = 0
i = 0

def click_and_crop(event, x, y, flags, param):
	# grab references to the global variables
	global refPt, cropping,image,i
 
	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
	if event == cv2.EVENT_LBUTTONDOWN:
		refPt = [(x, y)]
		cropping = True
 
	# check to see if the left mouse button was released
	elif event == cv2.EVENT_LBUTTONUP:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
		refPt.append((x, y))
		cropping = False
 
		# draw a rectangle around the region of interest
		cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
		imageq = "image{0}".format(str(i))
		sql = "INSERT INTO user_points VALUES('{0}','{1}','{2}','{3}','{4}')".format(imageq,refPt[0][0],refPt[0][1],refPt[1][0],refPt[1][1])
		cursor.execute(sql)
		conn.commit()
		cv2.imshow("image", image)


def user_input():
	global image,i
	image = cv2.imread("image{0}.jpg".format(str(i)))
	clone = image.copy()
	cv2.namedWindow("image")
	cv2.setMouseCallback("image", click_and_crop)
	while True:
	# display the image and wait for a keypress
		cv2.imshow("image", image)
		key = cv2.waitKey(1) & 0xFF
 
	# if the 'c' key is pressed, break from the loop
		if key == ord("c"):
			break

def haar_test():
	global image,i
	image = cv2.imread("image{0}.jpg".format(str(i)))
	face = detector.detect(image)
	for (x, y, w, h) in face:
		imageq = "image{0}".format(str(i))
		sql = "INSERT INTO haar_points VALUES('{0}','{1}','{2}','{3}','{4}')".format(imageq,x,y,x+w,y+h)
		cursor.execute(sql)
		conn.commit()

def aprox():
	global i
	sql = "image{0}".format(str(i))
	for row_user in cursor.execute("SELECT * from user_points WHERE image = '{0}'".format(sql)):
			print()
	for row_haar in cursor.execute("SELECT * from haar_points WHERE image = '{0}'".format(sql)):
			print()
	S_user =(row_user[3] - row_user[1])*(row_user[4] - row_user[2])
	S_haar =(row_haar[3] - row_haar[1])*(row_haar[4] - row_haar[2])
	user = list(row_user)
	haar = list(row_haar)
	#print(user)
	if row_haar[1] < row_user[1]:
		haar[1] = user[1]
	if row_haar[2] < row_user[2]:
		haar[2] = user[2]
	if row_haar[3] > row_user[3]:
		haar[3] = user[3]
	if row_haar[4] > row_user[4]:
		haar[4] = user[4]
	Smal = (haar[3] - haar[1])*(haar[4] - haar[2])

	k = Smal/(S_haar+S_user - Smal)
	print(sql + " : " + str(k))
	#l1y = 
	#s_inlying =

if __name__ == "__main__":
	
	detector = Detector.HaarDetector() 
	for i in range(10):
		user_input()
		#haar_test()
		aprox()
import cv2

cap=cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,960)

while True:
	ret, frame=cap.read()
	if ret:
		cv2.imshow('camera0',frame)

	if cv2.waitKey(1)&0xFF==ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
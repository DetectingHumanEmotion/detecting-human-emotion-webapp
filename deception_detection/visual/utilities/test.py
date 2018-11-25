import cv2


start_angle=0
end_angle=180
arc_dev=5
face_pts = cv2.ellipse2Poly((150,100), (45,85),0,  start_angle,end_angle, arc_dev)
# print(face_pts)
# (x,y)=face_pts
# print("x:",x,"y:",y)
print("THIRDDDDDDDDDDDDDDDD: ",face_pts[3])
# draw the detected bounding boxes on the images
# You can modify this to also draw a label.
left=100;
right=200;
top=100;
bottom=200;
p1 = (int(left), int(top))
p2 = (int(right), int(bottom))

# #study how ellipse to poly works
# i=0
# for face_pt in face_pts:
#     print(face_pt)
#     print(i)
#     i=i+1
#     """
#     face_pts = cv2.ellipse2Poly((150,100), (45,85),0,  0,180, 5) 180/5==36
#     face_pts = cv2.ellipse2Poly((150,100), (45,85),0,  0,180, 10) 180/10==18
#     face_pts = cv2.ellipse2Poly((150,100), (45,85),0,  30,180, 10) (180-30)/10=15
#     """

number_of_points=len(face_pts)
print(number_of_points)

"""
print(face_pts[i],face_pts[-i])
[195 100] [195 100]
[194 115] [105 100]
[192 129] [106 115]
[189 142] [108 129]
[184 155] [111 142]
[179 165] [116 155]
[172 174] [121 165]
[165 180] [128 174]
[158 184] [135 180]
[150 185] [142 184]
"""
i=0
while i <= (number_of_points/4 + 4):
    (x1, y1) = face_pts[i]
    (x2, y2) = face_pts[i + 1]
    (x3, y3) = face_pts[-i - 2]
    (x4, y4) = face_pts[-i - 1]
    """
    x4,y4 -- x1,y1          L,T -- L+(R-L/2),T -- R,T
      |        |             |                     |
    x3,y3 -- x2,y2        L,T+(B-T/2)          R,T+(B-T/2)
    """
    # print(i,face_pts[i], face_pts[i+1])face_pts[-i-1], face_pts[-i])
    print(i,face_pts[-i-1], face_pts[i])
    print(i,face_pts[-i-2], face_pts[i+1])
    x_half = (right - left) / 2
    y_half = (bottom - top) / 2

    xx = left
    yy = top
    if ((xx <= x2) and (xx >= x3) and (yy >= y1) and (yy >= y2)):
        print("found", str(datetime.now()))

    xx = left + x_half
    if ((xx <= x2) and (xx >= x3) and (yy >= y1) and (yy >= y2)):
        print("found", str(datetime.now()))

    xx = right
    yy = top
    if ((xx <= x2) and (xx >= x3) and (yy >= y1) and (yy >= y2)):
        print("found", str(datetime.now()))

    xx = left
    yy = top + y_half
    if ((xx <= x2) and (xx >= x3) and (yy >= y1) and (yy >= y2)):
        print("found", str(datetime.now()))

    xx = right
    yy = top + y_half
    if ((xx <= x2) and (xx >= x3) and (yy >= y1) and (yy >= y2)):
        print("found", str(datetime.now()))

    i=i+1

# for face_pt in face_pts:
#     (x,y)=face_pt


# for face_pt in face_pts:
#     (x,y)=face_pt
#     # if (p1==(x,y)) or (p2==(x,y)):
#     if (x>left) and (x<right) and (y<top) and (y>bottom):
#         print("hand touched face")
#         print("Top left corner: ", p1)
#         print("Bottom right corner: ", p2)
#         print("--------------")
#     else:
#         print("nope x:",x,"y",y)
#         data_type_compatibility_check_x=x-left;
#         data_type_compatibility_check_y=y-top;
#         print("check:",data_type_compatibility_check_x,data_type_compatibility_check_y)

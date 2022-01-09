from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import numpy as np
import cv2
import os

h = 450
w = 800


def initCrop(img, l, u, r, d):
    img = img.crop((l, u, img.size[0]-r, img.size[1]-d))
    return img


def imgReshape(img):
    d = 1
    img = initCrop(img, 0, img.size[1]//2, 0, img.size[1]//3)
    img = img.resize((w, h), Image.ANTIALIAS)
    if d == 1:
        img = img.convert('L')

    img = np.array(img)
    return img.reshape((h, w, d))


def findWalls(img_np, no_lines=11, threshold=50):
    h, w, d = img_np.shape
    dx = w//no_lines

    # center for lidar
    x1 = 400
    y1 = 0

    distances = []
    start_points = range(dx//2, w, dx)
    for start_point in start_points:
        distance = h - 1
        while distance >= 0:
            if img_np[distance][start_point] <= threshold:  # pixel threshold
                break
            distance -= 1
        distance = h - distance - 1
        #distance=y2 , start_point = x2
        distances.append(getDistance(x1, y1, start_point, distance))
        # distances.append(distance) #* 1.0 / h)

    # print(np.round(distances))
    return np.round(distances)


def getDistance(x1, y1, x2, y2):
    #print(x1, y1, x2, y2)
    return np.sqrt(np.power((y2-y1), 2)+np.power((x2-x1), 2))


def getMesuresDistances(img):
    img_np = imgReshape(img)
    return findWalls(img_np)


def getMesuresFromPath(path):
    image = Image.open(path)
    return getMesuresDistances(image)

# path = "./mytest/images/"+"9_19.jpg"

# getMesuresFromPath(path)

from google.colab import files
uploaded = files.upload()

images = sorted(uploaded.keys())

print("Order of the images:")
for name in images:
  print(name)

import cv2

fps = 4
output_video = "simulation.mp4"

image0 = cv2.imread(images[0])
height, width, layers = image0.shape
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

video = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

for image in images:

  frame = cv2.imread(image)
  frame = cv2.resize(frame, (width, height))
  video.write(frame)

video.release()

print("Video generated: ", output_video)

files.download(output_video)

output_video_horizontal = "simulation_horizontal.mp4"

target_w, target_h = 1280, 720

cap = cv2.VideoCapture(output_video)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')

video_horizontal = cv2.VideoWriter(output_video_horizontal, fourcc, fps, (target_w, target_h))

import numpy as np

while True:
    ret, frame = cap.read()
    if not ret:
        break

    canvas = np.zeros((target_h, target_w, 3), dtype=np.uint8)
    x_offset = (target_w - width) // 2
    y_offset = (target_h - height) // 2
    canvas[y_offset:y_offset+height, x_offset:x_offset+width] = frame
    video_horizontal.write(canvas)

cap.release()
video_horizontal.release()

print("Horizontal video generated:", output_video_horizontal)

files.download(output_video_horizontal)

import os

i=0
for image in images:
  if os.path.exists(image):
    os.remove(image)
  else:
    i+=1

if i==0:
  print("All images found and deleted")

# ffmpeg -i VPC019.avi -strict -2 cam19.mp4
# ffmpeg -i VPC020.avi -strict -2 cam20.mp4
# ffmpeg -i VPC023.avi -strict -2 cam23.mp4
# ffmpeg -i VPC069.avi -strict -2 cam69.mp4
# ffmpeg -i VPC071.avi -strict -2 cam71.mp4

# ffmpeg -i M002_141534.mp4 -r 30 -s 960x540 -strict -2 cam102.mp4
# ffmpeg -i M003_141520_incont.mp4 -r 30 -s 960x540 -strict -2 cam103.mp4
# ffmpeg -i M006_141552.mp4 -r 30 -s 960x540 -strict -2 cam106.mp4

ffmpeg -i cam19.mp4 -r 30 -s 960x540 -strict -2 cam19_2.mp4
ffmpeg -i cam20.mp4 -r 30 -s 960x540 -strict -2 cam20_2.mp4
ffmpeg -i cam22.mp4 -r 30 -s 960x540 -strict -2 cam22_2.mp4
ffmpeg -i cam23.mp4 -r 30 -s 960x540 -strict -2 cam23_2.mp4
ffmpeg -i cam69.mp4 -r 30 -s 960x540 -strict -2 cam69_2.mp4
ffmpeg -i cam71.mp4 -r 30 -s 960x540 -strict -2 cam71_2.mp4

ffmpeg -i M003_141520_incont.mp4 -r 30 -s 960x540 -strict -2 cam103.mp4
# ffmpeg -i M002_141534.mp4 -r 30 -s 960x540 -strict -2 cam102.mp4
ffmpeg -i M006_141520_incont.mp4 -r 30 -s 960x540 -strict -2 cam103.mp4
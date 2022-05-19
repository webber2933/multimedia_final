from fer import Video
from fer import FER

video_filename = "toadstool/toadstool/participants/participant_0/participant_0_video.avi"
video = Video(video_filename)

# Analyze video, displaying the output
detector = FER(mtcnn=True)
raw_data = video.analyze(detector, display=True)
df = video.to_pandas(raw_data)
print(df)
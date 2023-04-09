import pytube
# importing packages
from pytube import YouTube
import os

# url input from user
yt = YouTube(
	str(input("Enter the URL of the video you want to download: \n>> ")))

# check for destination to save file
print("Enter the destination (leave blank for current directory)")
destination = str(input(">> ")) or '.'

action = input("Pls indicate the type (mp3/mp4): \n>> ").lower()

if action == 'mp3':
	video = yt.streams.filter(only_audio=True).first()
	# download the file
	out_file = video.download(output_path=destination)
	options = {
		'format': 'bestaudio/best',
		'keepvideo': False,
	}

	# save the file
	base, ext = os.path.splitext(out_file)
	new_file = base + '.mp3'
	# new_file = base + '.mp4'
	os.rename(out_file, new_file)

elif action == 'mp4':
	#video = yt.streams.filter(only_audio=False).first()
	video = yt.streams.get_highest_resolution()

	x1 = yt.streams.get_by_resolution('720p')
	print(x1)
	#yt.streams.filter(progressive=True)
	#x2 = yt.streams.get_by_resolution('1080p')
	#print(x2)

	# download the file
	out_file = video.download(output_path=destination)
	options = {
		'format': 'bestaudio/best',
		'keepvideo': False,
		#'keepvideo': True,
		#'outtmpl': filename,
	}

	# save the file
	base, ext = os.path.splitext(out_file)
	# new_file = base + '.mp3'
	new_file = base + '.mp4'
	os.rename(out_file, new_file)

else:
	print("Pls select again!")
	exit()

# result of success
print(yt.title + "has been successfully downloaded.")

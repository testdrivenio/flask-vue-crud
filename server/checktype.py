def checkType(name):
	video_accepted_types = ['mp4','webm','ogg']
	image_accepted_types = ['gif','jpg','png', 'jpeg']
	extension=name.split('.')[1]
 
	if extension in image_accepted_types:
		return 'Image'
	
	elif extension in video_accepted_types:
		return 'video'

	else:
		return 'notAcceptedType'

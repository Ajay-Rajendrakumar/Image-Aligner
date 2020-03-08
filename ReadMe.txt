		Image processing
Objective:
-From the sample/test images provided, you have to identify the features andalign the images according to the original.
-The test images may be scaled, offset or rotated or a combination of these.
-Ideally, the test image should be aligned to the original image in the sameorientation and scale.
-You may use any language of your preference to accomplish this task.



Folders:
	Source_img = Folder contains Original Image
	Test_imgs = Folder contains Collection of Test Images
	Aligned_imgs = Folder contains Collection of Aligned Images after processing

Approach:
	-Used Oriented FAST and Rotated BRIEF(ORB) algorithm for matching original image and Test images.
	-Used Homography matrix with cv2.warpPerspective Function for image transformations.

pros:
	-Can resolve(align) Scaled , Translated and Rotated images.
	-ORB enable quick computation time(for matching images).
cons:
	-Can process only one original file at a time (ie. for new original file old file needed to be deleted).
	-if original image is completely different from test images(mismatch),jpg files with trash contents are stored in Aligned_imgs.
		

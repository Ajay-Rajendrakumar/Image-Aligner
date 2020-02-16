import cv2
import numpy as np
import glob
import os

def Fix_Img(test,src):

	#Image Matching using ORB
	Orb = cv2.ORB_create(edgeThreshold=15, patchSize=31, nlevels=8, fastThreshold=20, scaleFactor=1.2, WTA_K=2,scoreType=cv2.ORB_FAST_SCORE, firstLevel=0, nfeatures=1000)
	Test_Locator, Test_descriptor = Orb.detectAndCompute(test, None)
	Src_Locator, Src_descriptor = Orb.detectAndCompute(src, None)
	
	  	# Matching Src and Test img Descriptors
	DescMatch = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
	MatchedDesc = DescMatch.match(Test_descriptor,Src_descriptor, None)

	#Sort Descriptors(for identifying better matches) 
	MatchedDesc.sort(key=lambda dist: dist.distance, reverse=False)

	#Extract Better Matches
	Number_of_best_matches = int(len(MatchedDesc)* .20)
	MatchedDesc = MatchedDesc[:Number_of_best_matches]

	
	# Extract location of best descriptor matches
	Src_pt= np.zeros((len(MatchedDesc), 2), dtype=np.float32)
	Test_pt = np.zeros((len(MatchedDesc), 2), dtype=np.float32)
	
	for iterator, value in enumerate(MatchedDesc):
		Test_pt[iterator, :] = Test_Locator[value.queryIdx].pt
		Src_pt[iterator, :] = Src_Locator[value.trainIdx].pt


   	#Homography
	Homography, mask = cv2.findHomography(Test_pt, Src_pt, cv2.RANSAC)
	return Homography




if __name__ == '__main__':

	Align_counter=0
	if(os.path.exists('Source_img/Original.jpg')==False):
		print("Sorry, No Source file found!")
	else:
		#Reading Source(original) Image from directory
		Source_img = cv2.imread('Source_img/Original.jpg', cv2.IMREAD_COLOR)
		Gsrc = cv2.cvtColor(Source_img, cv2.COLOR_BGR2GRAY)

		#Reading Test image(files) from Directory
		Test_parent_dir = 'Test_imgs/'
		TestImg_File = [os.path.basename(f) for f in glob.glob(os.path.join(Test_parent_dir, '*.jpg'))]
		if(len(TestImg_File) == 0):
			print("Sorry, No Test file(s) found!")
		else:
			for test_idx in range(len(TestImg_File)):
				
				ImgFile = TestImg_File[test_idx]
				Test_img = cv2.imread('Test_imgs/'+ ImgFile, cv2.IMREAD_COLOR)

				#Convert given img to grayscale
				Gtest = cv2.cvtColor(Test_img, cv2.COLOR_BGR2GRAY)

				#Aligning TestImage
				Homography = Fix_Img(Gtest,Gsrc)
				height, width, channels = Source_img.shape
				Res_img = cv2.warpPerspective(Test_img, Homography, (width, height))

				#Saving Altered Image
				FileName = "Aligned_imgs/" + ImgFile[ : -4] + "_Altered.jpg"
				Align_counter += 1
				cv2.imwrite(FileName,Res_img)
	print("Number of Aligned Files: ",Align_counter)

#end
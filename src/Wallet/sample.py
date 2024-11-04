import cv2
import fingerprint_feature_extractor

im = cv2.imread("2.jpg",0)

FT,FB = (
    fingerprint_feature_extractor.extract_minutiae_features(
        im,
        spuriousMinutiaeThresh=10,
        invertImage=False,
        showResult=True,
        saveResult=True,
    )
)

print(FB,FT)
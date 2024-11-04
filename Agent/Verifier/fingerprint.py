import fingerprint_feature_extractor
from fingerprint_feature_extractor import MinutiaeFeature
import cv2


class Fingerprint:
    def __init__(self):
        pass

    def __generate__(self, image_path):
        img = cv2.imread(image_path, 0)
        FeaturesTerminations, FeaturesBifurcations = (
            fingerprint_feature_extractor.extract_minutiae_features(
                img,
                spuriousMinutiaeThresh=10,
                invertImage=False,
                showResult=False,
                saveResult=True,
            )
        )
        _temp = []
        _bifuc = []
        for x in FeaturesTerminations:
            if hasattr(x, "__dict__"):
                attributes = x.__dict__
                _temp.append(
                    [
                        int(attributes["locX"]),
                        int(attributes["locY"]),
                        attributes["Orientation"],
                    ]
                )

        for x in FeaturesBifurcations:
            if hasattr(x, "__dict__"):
                attributes = x.__dict__
                _bifuc.append(
                    [
                        int(attributes["locX"]),
                        int(attributes["locY"]),
                        attributes["Orientation"],
                    ]
                )

        return {"terminations": _temp, "bifurcations": _bifuc}

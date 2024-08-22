from dataclasses import dataclass
from typing import Dict, Optional

from ._BBox import BBox
from ._Polygon import Polygon


@dataclass
class ObjectPrediction:
    """
    A single object prediction.
    """
    # The score given to the prediction
    score: Optional[float] = None

    # The predicted label of the object
    label: str = None

    # The bounding box around the prediction
    bbox: BBox = None

    # The polygon around the prediction
    polygon: Polygon = None

    # Any meta-data
    meta: Optional[Dict[str, str]] = None

    def __str__(self):
        """
        Returns a short string representation of itself.

        :return: the string representation
        :rtype: str
        """
        return "label=%s, score=%s" % (self.label, str(self.score))

    def to_dict(self):
        """
        Returns its values as dictionary.

        :return: the generated dictionary
        :rtype: dict
        """
        result = {
            "label": self.label,
            "bbox": self.bbox.to_dict(),
            "polygon": self.polygon.to_dict(),
        }
        if self.score is not None:
            result["score"] = self.score
        if self.meta is not None:
            result["meta"] = self.meta
        return result

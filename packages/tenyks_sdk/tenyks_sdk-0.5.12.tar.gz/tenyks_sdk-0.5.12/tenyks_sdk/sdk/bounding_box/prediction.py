from typing import Dict, List

from pydantic import Field, NonNegativeFloat

from tenyks_sdk.sdk.bounding_box import Annotation
from tenyks_sdk.sdk.category import Category
from tenyks_sdk.sdk.tag import Tag, strings_to_tags


class Prediction(Annotation):
    score: NonNegativeFloat = Field(
        description="Confidence score of the prediction",
        examples=[0.75, 1.0, 0.5],
        le=1.0,
    )

    class Config:
        protected_namespaces = ()  # Override to avoid pydantic warning about model_

    @classmethod
    def convert_tags_category_and_create(
        cls,
        prediction: Dict,
        dataset_tags: List[Tag],
        dataset_categories: List[Category],
        convert_to_xywh: bool = False,
    ):
        converted_tags = strings_to_tags(prediction.get("tags", []), dataset_tags)
        converted_category = dataset_categories[prediction.get("category_id")]
        if convert_to_xywh:
            prediction["coordinates"] = [
                prediction["coordinates"][0],
                prediction["coordinates"][1],
                prediction["coordinates"][2] - prediction["coordinates"][0],
                prediction["coordinates"][3] - prediction["coordinates"][1],
            ]
        return cls(
            coordinates=prediction.get("coordinates"),
            category=converted_category,
            id=prediction.get("bbox_id") or prediction.get("id"),
            segmentation=prediction.get("segmentation", []),
            tags=converted_tags,
            score=prediction.get("score"),
        )

    def to_coco_dict(self, image_id: str) -> dict:
        return {
            "id": self.id,
            "image_id": image_id,
            "category_id": self.category.id,
            "bbox": self.coordinates,
            "segmentation": self.segmentation,
            "score": self.score,
            "iscrowd": 0,
            "tags": [tag.model_dump() for tag in self.tags],
        }

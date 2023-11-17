import supervision as sv
from autodistill_gpt_4v import GPT4V
from autodistill.detection import CaptionOntology
from autodistill_grounded_sam import GroundedSAM
from autodistill.core.custom_detection_model import CustomDetectionModel
import cv2

classes = ["mercedes", "toyota"]


SAMGPT = CustomDetectionModel(
    detection_model=GroundedSAM(
        CaptionOntology({"car": "car"})
    ),
    classification_model=GPT4V(
        CaptionOntology({k: k for k in classes})
    )
)

IMAGE = "C:/edema_macular_diabetico/project/datasets/eye-tracking-code/ODIR-5K/ODIR-5K/myodir-crop/1_left.jpg"

results = SAMGPT.predict(IMAGE)

image = cv2.imread(IMAGE)

annotator = sv.MaskAnnotator()
label_annotator = sv.LabelAnnotator()

labels = [
    f"{classes[class_id]} {confidence:0.2f}"
    for _, _, confidence, class_id, _ in results
]

annotated_frame = annotator.annotate(
    scene=image.copy(), detections=results
)
annotated_frame = label_annotator.annotate(
    scene=annotated_frame, labels=labels, detections=results
)

sv.plot_image(annotated_frame, size=(8, 8))
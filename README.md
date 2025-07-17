# Extended-OKS COCO Evaluation API

This repository extends the standard COCO person keypoint evaluation by implementing the Extended-OKS (Ex-OKS) metric introduced in the ProbPose paper. Built on top of the original [xtcocotools](https://github.com/jin-s13/xtcocoapi/) and the official [COCO API](https://github.com/cocodataset/cocoapi), Ex-OKS remains fully backward-compatible with the standard OKS. It adds support for:

- Out-of-image keypoints (points annotated outside the image boundary or activation window) to asses model's robustness
- Per-visibility-level mAP breakdowns to pinpoint which keypoints cause errors

### Extended-OKS vs. OKS

- **OKS (Object Keypoint Similarity)** measures similarity between predicted and ground-truth keypoints within the image.
- **Ex-OKS (Extended OKS)** extends OKS by:
  - Penalizing in-image predictions when the ground-truth is out-of-image
  - Penalizing out-of-image predictions when the groud-truth is in-image
  - The same as OKS when both ground-truth and prediction are in-image

## Detailed Explanation

**TODO** -- *Add mathematical definitions, design decisions, and API details here.*

## Usage / Demo

```python
from ExCocotools.coco import COCO
from ExCocotools.cocoeval import COCOeval

# Standard OKS evaluation (backward-compatible)
cocoEval = COCOeval(cocoGt_json, cocoDt_json, iouType='keypoints', extended_oks=False)

# --- OR ---

# Extended-OKS evaluation
cocoEval = COCOeval(cocoGt_json, cocoDt_json, iouType='keypoints', extended_oks=True)

# Evaluate and print results
cocoEvalExt.evaluate()
cocoEvalExt.accumulate()
cocoEvalExt.summarize()
```

For more details, see [COCO Demo](demos/demo_coco.py) or [CropCOCO Demo](demos/demo_cropcoco.py) files.

## Installation

### From PyPI

```bash
pip install ExCocotools
```

### From Source

```bash
git clone https://github.com/MiraPurkrabek/Ex-cocotools
cd Ex-cocotools
pip install -r requirements.txt
pip install -e .
```

## Acknowledgements and Citation

This implementation builds upon the COCO API and xtcocotools projects. The Extended-OKS metric and its evaluation methodology are described in the ProbPose paper:

```bibtex
@InProceedings{Purkrabek2025CVPR,
    author    = {Purkrabek, Miroslav and Matas, Jiri},
    title     = {ProbPose: A Probabilistic Approach to 2D Human Pose Estimation},
    booktitle = {Proceedings of the Computer Vision and Pattern Recognition Conference (CVPR)},
    month     = {June},
    year      = {2025},
    pages     = {27124-27133}
}
```
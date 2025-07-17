<!-- omit in toc -->
</h1><div id="toc">
  <ul align="center" style="list-style: none; padding: 0; margin: 0;">
    <summary>
      <h1 style="margin-bottom: 0.0em;">
        ExOCocoTools - Extended-OKS for COCO Evaluation API
      </h1>
    </summary>
  </ul>
</div>
</h1><div id="toc">
</div>


This repository extends the standard COCO person keypoint evaluation by implementing the Extended-OKS (Ex-OKS) metric introduced in the [ProbPose paper](https://mirapurkrabek.github.io/ProbPose/). Built on top of the original [xtcocotools](https://github.com/jin-s13/xtcocoapi/) and the official [COCO API](https://github.com/cocodataset/cocoapi), Ex-OKS remains fully backward-compatible with the standard OKS. It adds support for:

- Out-of-image keypoints (points annotated outside the image boundary or activation window) to asses model's robustness
- Per-visibility-level mAP breakdowns to pinpoint which keypoints cause errors

Why ExOCocoTools? ExO stands both for Ex-OKS and for greek "exo", meaning "outside". This evaluation protocol is the first to evaluate on keypoints outside of the image.

<!-- omit in toc -->
## Table of Contents

- [Extended-OKS vs. OKS](#extended-oks-vs-oks)
- [Visibility Levels](#visibility-levels)
- [Usage / Demo](#usage--demo)
- [Installation](#installation)
- [Acknowledgements and Citation](#acknowledgements-and-citation)

## Extended-OKS vs. OKS

- **OKS (Object Keypoint Similarity)** measures similarity between predicted and ground-truth keypoints within the image.
- **Ex-OKS (Extended OKS)** extends OKS by:
  - Penalizing in-image predictions when the ground-truth is out-of-image
  - Penalizing out-of-image predictions when the groud-truth is in-image
  - The same as OKS when both ground-truth and prediction are in-image


|Aspect|**OKS**|**Ex-OKS**|
|:---:|:---:|:---:|
|What it measures   | Alignment of predictions vs. ground-truth using a Gaussian fall-off based on object scale | Same alignment AND corectness of "in-view" vs. "out-of-view" classification |
| Presence handling | Only evaluates localization for keypoints inside the image | Localization for keypoints inside the image and classification for out-of-view keypoints |
| False-positive penalty| None | Penalizes in-image prediction when a keypoint is out-of-view |
| Primary use-case| Benchmark evaluation: Localize all points inside the image | Real-world applications: First predict if the point is "there" and if yes, localize it |


<!-- omit in toc -->
### Detailed Explanation

Formally, Ex-OKS has the same form as OKS -- euclidean distance scaled by image scale and per-keypoint sigma.

```math
    \text{Ex-OKS} = \exp{(\frac{-d_{i}^2}{2k^2\sigma^2})}
```

However, for Ex-OKS, the distance $d_i$ depends on the situation (ground-truth in/out; precition in/out). Below, you can see formal defintion along with illustrative scheme. 

```math
d_i = \begin{cases}
        d_e(x^{*}_i, x'_i) & \text{if } p^{*}_p = 1 \text{ and } p'_p = 1 \\
        d_e(\text{AW}, x'_i) & \text{if } p^{*}_p = 0 \text{ and } p'_p = 1 \\
        d_e(x^{*}_i, \text{AW}) & \text{if } p^{*}_p = 1 \text{ and } p'_p = 0 \\
        0                               & \text{else} 
    \end{cases} \\
```

<p align="center">
    <img src="assets/exoks_scheme.png" width="500" alt="Extended-OKS Scheme">
</p>

In summary, Ex-OKS *extends* OKS to situation when ground-truth or prediction are outside of the activation window. For more details, read the full explanation in the [ProbPose paper](https://mirapurkrabek.github.io/ProbPose/static/pdfs/ProbPose.pdf).

## Visibility Levels

Apart from Ex-OKS, this library also shows mAP for different visibility levels.
Best demonstrated in [CropCOCO Demo](demos/demo_cropcoco.py), rows with specific visibility show performance for such keypoints.

<p align="center">
    <img src="assets/visibility_levels.png" width="500" alt="mAP for different visibility levels">
</p>

The output above shows that for
- occluded keypoints (v=1), the mAP is 38.9
- for visible keypoints (v=2), the mAP is 79.1
- and for out-of-image keypoints (v=3), the mAP is 31.7

## Usage / Demo

```python
from exococotools.coco import COCO
from exococotools.cocoeval import COCOeval

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

<!-- omit in toc -->
### From PyPI

```bash
pip install exococotools
```

<!-- omit in toc -->
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
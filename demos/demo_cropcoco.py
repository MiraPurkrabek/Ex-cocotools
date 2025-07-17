from exococotools.coco import COCO
from exococotools.cocoeval import COCOeval
import numpy as np

gt_file = '../annotations/example_cropcoco_val.json'
preds = '../annotations/example_cropcoco_preds.json'

sigmas = np.array(
                [.26, .25, .25, .35, .35, .79, .79, .72, .72, .62,.62, 1.07, 1.07, .87, .87, .89, .89])/10.0

cocoGt = COCO(gt_file)
cocoDt = cocoGt.loadRes(preds)
cocoEval = COCOeval(cocoGt, cocoDt, 'keypoints', sigmas, use_area=True, extended_oks=True, confidence_thr=0.5, padding=1.25)
cocoEval.evaluate() 
cocoEval.accumulate()
cocoEval.summarize()

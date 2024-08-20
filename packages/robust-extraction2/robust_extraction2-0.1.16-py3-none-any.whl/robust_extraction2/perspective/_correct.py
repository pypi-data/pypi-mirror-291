from typing_extensions import Unpack
import numpy as np
import cv2 as cv
import pure_cv as vc
from robust_extraction2 import Corners, vectors as vec

def pad(corners: Corners, *, padx: float, pady: float) -> Corners:
  """Pad perspective corners, by:
  1. Move the centroid to 0
  2. Scale by `[1+padx, 1+pady]`
  3. Move back to original position
  """
  centroid = corners.mean(axis=0)
  return (corners - centroid) * np.array([1+padx, 1+pady]) + centroid

def correct(img: vc.Img, corners: Corners) -> vc.Img:
  """Correct image perspective (from absolute corners)"""
  tl, tr, br, bl = np.array(corners)
  w = int((vec.dist(tl, tr) + vec.dist(bl, br)) / 2)
  h = int((vec.dist(tl, bl) + vec.dist(tr, br)) / 2)
  src = np.array([tl, tr, br, bl])
  dst = np.array([[0, 0], [w, 0], [w, h], [0, h]])
  M = cv.getPerspectiveTransform(src.astype(np.float32), dst.astype(np.float32))
  return cv.warpPerspective(img, M, (w, h)) 

def correct_perspective(img: vc.Img, corners: Corners):
    """Correct image perspective
    - `corners`: relative corners (i.e. [1, 1] is the image's bottom right)
    """
    h, w = img.shape[:2]
    rescaled_corners = np.array(corners)*[w, h]
    return correct(img, rescaled_corners)
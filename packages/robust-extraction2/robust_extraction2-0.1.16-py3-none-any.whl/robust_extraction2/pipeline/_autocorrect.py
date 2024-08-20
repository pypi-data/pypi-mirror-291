from typing_extensions import Unpack
import numpy as np
from haskellian import either as E
import pure_cv as vc
from robust_extraction2 import ExtendedModel, Corners, \
  lines as ls, pipeline as pipe, perspective as pve
from robust_extraction2.lines.cluster import IntersectError
from .params import Params

def detect_corners(img: vc.Img, model: ExtendedModel, **params: Unpack[pipe.Params]):
  rows, cols = pipe.head(img, model, **params)
  return ls.cluster.intersect_clusters(rows, cols)

@E.do[IntersectError]()
def descaled_detect_corners(img: vc.Img, model: ExtendedModel, *, descale_h = 1920, **params: Unpack[pipe.Params]) -> Corners:
  """Detects perspective corners in the descaled image and rescales them back to the original image."""
  s = img.shape[0] / descale_h
  rescaled_img = vc.rescale_h(img, descale_h)
  corners = detect_corners(rescaled_img, model, **params).unsafe()
  return np.round(s*np.array(corners)).astype(int)

@E.do[IntersectError]()
def autocorrect(img: vc.Img, model: ExtendedModel, *, descale_h = 1920, **params: Unpack[Params]) -> tuple[vc.Img, Corners]:
  raw_corners = descaled_detect_corners(img, model, descale_h=descale_h, **params).unsafe()
  px, py = params.get('correction_pads') or (0.04, 0.04)
  corners = pve.pad(raw_corners, padx=px, pady=py)
  return pve.correct(img, corners), corners
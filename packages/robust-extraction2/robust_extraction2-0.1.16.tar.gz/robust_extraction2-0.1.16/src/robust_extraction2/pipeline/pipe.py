from typing_extensions import Unpack, TypedDict
from haskellian import either as E
import pure_cv as vc
from robust_extraction2 import ExtendedModel, pipeline as pipe
from .params import Params

Error = pipe.IntersectError | pipe.ExtractionError

class Result(TypedDict):
  corr_img: vc.Img
  cnts: vc.Contours
  corners: vc.Corners | None

@E.do[Error]()
def extract(
  img: vc.Img, model: ExtendedModel, *, autocorrect: bool = True,
  autocorrect_h: int = 1920, autoextract_h: int = 1920,
  **params: Unpack[Params]
):
  if autocorrect:
    corr, corners_arr = pipe.autocorrect(img, model, descale_h=autocorrect_h, **params).unsafe()
    tl, tr, br, bl = corners_arr.tolist()
    corners = vc.Corners(tl=tl, tr=tr, br=br, bl=bl)
  else:
    corr = img
    corners = None
  cnts = pipe.autoextract(corr, model, descale_h=autoextract_h, **params).unsafe()
  return Result(corr_img=corr, cnts=cnts.tolist(), corners=corners)
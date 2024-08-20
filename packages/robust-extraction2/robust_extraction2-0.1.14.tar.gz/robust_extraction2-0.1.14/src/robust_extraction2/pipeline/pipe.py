from typing_extensions import NotRequired, Unpack, TypedDict
from haskellian import either as E
from robust_extraction2 import Img, Contours, ExtendedModel, pipeline as pipe, Corners, Pads, DEFAULT_PADS
from .params import Params

Error = pipe.IntersectError | pipe.ExtractionError

class Perspective(TypedDict):
  corners: Corners
  pads: Pads

class Result(TypedDict):
  corr_img: Img
  cnts: Contours
  perspective: Perspective | None

@E.do[Error]()
def extract(
  img: Img, model: ExtendedModel, *, autocorrect: bool = True,
  autocorrect_h: int = 1920, autoextract_h: int = 1920,
  **params: Unpack[Params]
):
  if autocorrect:
    pads = params.get('correction_pads', DEFAULT_PADS)
    params = {**params, 'correction_pads': pads}
    corr, corners = pipe.autocorrect(img, model, descale_h=autocorrect_h, **params).unsafe()
    perspective = Perspective(corners=corners, pads=pads)
  else:
    corr = img
    perspective = None
  cnts = pipe.autoextract(corr, model, descale_h=autoextract_h, **params).unsafe()
  return Result(corr_img=corr, cnts=cnts, perspective=perspective)
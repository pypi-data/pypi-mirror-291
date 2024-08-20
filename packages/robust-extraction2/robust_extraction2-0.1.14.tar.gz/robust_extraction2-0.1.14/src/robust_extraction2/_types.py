from typing_extensions import TypeAlias, TypedDict, NamedTuple
from jaxtyping import Shaped
import numpy as np

Img2D: TypeAlias = Shaped[np.ndarray, "w h"]
Img3D: TypeAlias = Shaped[np.ndarray, "w h c"]
Img: TypeAlias = Img2D | Img3D

Contour: TypeAlias = Shaped[np.ndarray, 'N 2']
Contours: TypeAlias = Shaped[np.ndarray, 'N C 2']

Segment: TypeAlias = Shaped[np.ndarray, '1 4']
"""`1 x 4`: `[[x1, x2, y1, y2]]`"""

Segments: TypeAlias = Shaped[np.ndarray, 'N 1 4']
"""`N x 1 x 2`: `[[[x1, x2, y1, y2]], ...]`"""

Vec2: TypeAlias = Shaped[np.ndarray, '2']
Vecs2: TypeAlias = Shaped[np.ndarray, 'N 2']

class Corners(NamedTuple):
  tl: tuple[float, float]
  tr: tuple[float, float]
  br: tuple[float, float]
  bl: tuple[float, float]

class Pads(TypedDict):
  l: float; r: float; t: float; b: float

DEFAULT_PADS = Pads(l=0.02, r=0.02, t=0.02, b=0.02)
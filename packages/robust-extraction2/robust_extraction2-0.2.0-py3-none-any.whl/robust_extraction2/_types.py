from typing_extensions import TypeAlias
from jaxtyping import Shaped
import numpy as np

Contour: TypeAlias = Shaped[np.ndarray, 'N 2']
Contours: TypeAlias = Shaped[np.ndarray, 'N C 2']

Segment: TypeAlias = Shaped[np.ndarray, '1 4']
"""`1 x 4`: `[[x1, x2, y1, y2]]`"""

Segments: TypeAlias = Shaped[np.ndarray, 'N 1 4']
"""`N x 1 x 2`: `[[[x1, x2, y1, y2]], ...]`"""

Vec2: TypeAlias = Shaped[np.ndarray, '2']
Vecs2: TypeAlias = Shaped[np.ndarray, 'N 2']

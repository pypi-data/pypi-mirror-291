import numpy as np
import pure_cv as vc

def correct_perspective(img: vc.Img, corners: vc.Corners):
  """Correct image perspective
  - `corners`: relative corners (i.e. [1, 1] is the image's bottom right)
  """
  h, w = img.shape[:2]
  rescaled_corners = np.array(corners)*[w, h]
  return vc.corners.correct(img, rescaled_corners)
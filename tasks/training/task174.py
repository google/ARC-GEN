# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Generator."""

import common


def generate(rows=None, cols=None, idxs=None, colors=None, brows=None,
             bcols=None, size=10, num_boxes=3):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices of the boxes that should be placed
    colors: a list of colors to use for the boxes
    brows: a list of vertical coordinates where the boxes should be placed
    bcols: a list of horizontal coordinates where the boxes should be placed
    size: the size of the input and output grids
    num_boxes: the number of boxes to place
  """

  def is_symmetric(pixels):
    max_col = max([p[1] for p in pixels])
    for r, c in pixels:
      if (r, max_col - c) not in pixels: return False
    return True

  def is_rotational(pixels):
    max_row, max_col = max([p[0] for p in pixels]), max([p[1] for p in pixels])
    for r, c in pixels:
      if (max_row - r, max_col - c) not in pixels: return False
    return True

  if rows is None:
    wides = [common.randint(2, 5) for _ in range(num_boxes)]
    talls = [common.randint(2, 7 - wide) for wide in wides]
    while True:
      brows = [common.randint(0, size - tall) for tall in talls]
      bcols = [common.randint(0, size - wide) for wide in wides]
      if not common.overlaps(brows, bcols, wides, talls, 1): break
    rows, cols, idxs = [], [], []
    for idx in range(num_boxes):
      wide, tall = wides[idx], talls[idx]
      while True:
        num_pixels = common.randint(wide * tall // 2, wide * tall)
        pixels = common.continuous_creature(num_pixels, wide, tall)
        if is_symmetric(pixels) != (not idx): continue
        if is_rotational(pixels) != (not idx): continue
        break
      rows.extend([p[0] for p in pixels])
      cols.extend([p[1] for p in pixels])
      idxs.extend([idx] * len(pixels))
    colors = common.random_colors(num_boxes)

  width = max([c for c, i in zip(cols, idxs) if not i]) + 1
  height = max([r for r, i in zip(rows, idxs) if not i]) + 1
  grid, output = common.grid(size, size), common.grid(width, height)
  for r, c, idx in zip(rows, cols, idxs):
    grid[brows[idx] + r][bcols[idx] + c] = colors[idx]
    if not idx: output[r][c] = colors[idx]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1],
               cols=[0, 1, 2, 3, 1, 2, 0, 1, 1, 2, 3, 1, 2, 0, 2],
               idxs=[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2],
               colors=[6, 2, 7], brows=[6, 1, 2], bcols=[3, 1, 6]),
      generate(rows=[0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
               cols=[0, 1, 0, 1, 0, 1, 2, 0, 2, 3, 1, 2, 3, 4, 0, 1, 2],
               idxs=[0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2],
               colors=[4, 8, 2], brows=[1, 2, 7], bcols=[2, 6, 1]),
      generate(rows=[0, 0, 1, 1, 1, 1, 0, 0, 1, 2, 0, 0, 0, 1, 1, 1, 1, 1, 1],
               cols=[0, 3, 0, 1, 2, 3, 0, 1, 1, 1, 3, 4, 5, 0, 1, 2, 3, 5, 6],
               idxs=[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2],
               colors=[5, 3, 8], brows=[2, 1, 7], bcols=[5, 1, 0]),
  ]
  test = [
      generate(rows=[0, 0, 1, 1, 2, 2, 2, 2, 0, 0, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0,
                     1, 1, 1],
               cols=[1, 2, 1, 2, 0, 1, 2, 3, 0, 3, 0, 1, 2, 3, 3, 0, 1, 2, 3, 4,
                     0, 3, 4],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2,
                     2, 2, 2],
               colors=[9, 3, 4], brows=[2, 1, 7], bcols=[0, 5, 4]),
  ]
  return {"train": train, "test": test}

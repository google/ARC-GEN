# Copyright 2026 Google LLC
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


def generate(width=None, height=None, wides=None, talls=None, brows=None,
             bcols=None, prows=None, pcols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid.
    height: the height of the grid.
    wides: the widths of the boxes.
    talls: the heights of the boxes.
    brows: the rows of the boxes.
    bcols: the columns of the boxes.
    prows: the rows of the pixels.
    pcols: the columns of the pixels.
  """

  def draw():
    grid, output = common.grids(width, height)
    for wide, tall, row, col in zip(wides, talls, brows, bcols):
      common.hollow_rect(grid, wide, tall, row, col, 1)
      common.hollow_rect(output, wide, tall, row, col, 1)
      common.rect(output, wide - 2, tall - 2, row + 1, col + 1, 8)
    for group, (prow, pcol) in enumerate(zip(prows, pcols)):
      if prow < 0 or pcol < 0: continue
      r, c = brows[group] + prow, bcols[group] + pcol
      grid[r][c], output[r][c] = 0, 8
      rdir, cdir = 0, 0
      if prow == 0: rdir = -1
      if pcol == 0: cdir = -1
      if prow + 1 == talls[group]: rdir = 1
      if pcol + 1 == wides[group]: cdir = 1
      while True:
        r, c = r + rdir, c + cdir
        if r < 0 or c < 0 or r >= height or c >= width: break
        if output[r][c] != 0: return None, None
        output[r][c] = 8
        # Don't shoot too close to another box.
        if rdir == 0 and common.get_pixel(grid, r - 1, c) == 1: return None, None
        if rdir == 0 and common.get_pixel(grid, r + 1, c) == 1: return None, None
        if cdir == 0 and common.get_pixel(grid, r, c - 1) == 1: return None, None
        if cdir == 0 and common.get_pixel(grid, r, c + 1) == 1: return None, None
    return grid, output

  if width is None:
    width, height = common.randint(24, 28), common.randint(24, 28)
    num_boxes = common.randint(5, 6)
    while True:
      wides = [common.randint(3, 9) for _ in range(num_boxes)]
      talls = [common.randint(3, 9) for _ in range(num_boxes)]
      brows = [common.randint(1, height - t - 1) for t in talls]
      bcols = [common.randint(1, width - w - 1) for w in wides]
      if common.overlaps(brows, bcols, wides, talls, 1): continue
      prows, pcols = [-1] * num_boxes, [-1] * num_boxes
      for i in range(num_boxes):
        # Choose which side the "notch" should go (0 = no notch)
        side = common.randint(0, 4)
        if side in [1, 2] and talls[i] >= 5:
          prows[i] = common.randint(2, talls[i] - 3)
          pcols[i] = 0 if side == 1 else (wides[i] - 1)
        if side in [3, 4] and wides[i] >= 5:
          prows[i] = 0 if side == 3 else (talls[i] - 1)
          pcols[i] = common.randint(2, wides[i] - 3)
      if prows.count(-1) > 2: continue  # at most 2 boxes should be dormant.
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=25, height=24, wides=[6, 8, 7, 8, 6],
               talls=[6, 5, 6, 6, 4], brows=[1, 1, 8, 16, 17],
               bcols=[1, 15, 10, 2, 16], prows=[-1, 2, 2, 5, -1],
               pcols=[-1, 7, 0, 3, -1]),
      generate(width=28, height=24, wides=[7, 8, 9, 6, 6],
               talls=[5, 5, 7, 7, 5], brows=[1, 1, 7, 14, 18],
               bcols=[2, 19, 12, 5, 19], prows=[2, 2, 0, -1, -1],
               pcols=[0, 7, 3, -1, -1]),
  ]
  test = [
      generate(width=26, height=26, wides=[9, 9, 8, 7, 8, 5],
               talls=[6, 8, 6, 7, 6, 3], brows=[2, 3, 9, 13, 17, 22],
               bcols=[2, 16, 6, 16, 3, 14], prows=[-1, 0, 2, 6, 2, 2],
               pcols=[-1, 3, 0, 4, 0, 2]),
  ]
  return {"train": train, "test": test}

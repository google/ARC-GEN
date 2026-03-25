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


def generate(prow=None, pcol=None, brows=None, bcols=None, sizes=None,
             colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    prow: The row of the plus.
    pcol: The column of the plus.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    sizes: The sizes of the boxes.
    colors: The colors of the boxes.
  """

  def draw(alignment=None):
    grid, output = common.grids(16, 16, 7)
    # Draw the boxes.
    row_aligned, col_aligned = False, False
    for brow, bcol, size in zip(brows, bcols, sizes):
      common.rect(grid, size, size, brow, bcol, colors[1])
      common.rect(output, size, size, brow, bcol, colors[1])
      if size % 2 == 1:
        output[brow + size // 2][bcol + size // 2] = colors[0]
        if brow + size // 2 == prow: row_aligned = True
        if bcol + size // 2 == pcol: col_aligned = True
    # Avoid this case, it isn't defined in the problem suite.
    if row_aligned != col_aligned: return None, None
    if alignment is not None and row_aligned != alignment: return None, None
    # Draw the plus.
    for dr, dc in [(-1, 0), (0, -1), (0, 0), (1, 0), (0, 1)]:
      grid[prow + dr][pcol + dc] = colors[0]
      if row_aligned and col_aligned: output[prow + dr][pcol + dc] = colors[0]
    return grid, output

  if prow is None:
    num_boxes = common.randint(5, 10)
    colors = common.random_colors(2, exclude=[7])
    alignment = True if common.randint(0, 1) else False
    while True:
      prow, pcol = common.randint(1, 14), common.randint(1, 14)
      sizes = [common.randint(1, 7) for _ in range(num_boxes)]
      brows = [common.randint(0, 16 - s) for s in sizes]
      bcols = [common.randint(0, 16 - s) for s in sizes]
      if common.overlaps(brows + [prow], bcols + [pcol], sizes + [3], sizes + [3], 1): continue
      grid, _ = draw(alignment)
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(prow=3, pcol=5, brows=[3, 7, 7, 13, 14],
               bcols=[11, 3, 12, 13, 2], sizes=[3, 2, 4, 1, 2], colors=[8, 9]),
      generate(prow=14, pcol=14, brows=[0, 0, 0, 0, 5, 5],
               bcols=[0, 2, 5, 9, 0, 6], sizes=[1, 2, 3, 4, 5, 6],
               colors=[1, 8]),
      generate(prow=1, pcol=14, brows=[0, 3, 4, 6, 10, 11, 11, 14],
               bcols=[6, 2, 13, 5, 11, 1, 4, 13],
               sizes=[3, 1, 3, 2, 1, 1, 4, 2], colors=[3, 1]),
  ]
  test = [
      generate(prow=9, pcol=3, brows=[0, 1, 3, 5, 7, 9, 10, 11, 12, 14, 14],
               bcols=[0, 14, 13, 10, 10, 8, 10, 7, 5, 1, 14],
               sizes=[7, 1, 3, 1, 2, 1, 3, 2, 1, 1, 2], colors=[4, 8]),
  ]
  return {"train": train, "test": test}

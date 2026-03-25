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


def generate(size=None, rows=None, cols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    rows: The rows of the boxes.
    cols: The columns of the boxes.
    colors: The colors of the box pixels.
  """

  if size is None:
    size = common.randint(6, 16)
    num_boxes = 1
    if size >= 11 and size <= 12: num_boxes = 2
    if size >= 13 and size <= 14: num_boxes = 3
    if size >= 15 and size <= 16: num_boxes = 4
    while True:
      rows = [common.randint(0, size - 5) for _ in range(num_boxes)]
      cols = [common.randint(0, size - 5) for _ in range(num_boxes)]
      lengths = [5 for _ in range(num_boxes)]
      if not common.overlaps(rows, cols, lengths, lengths, 1): break
    colors = []
    for _ in range(num_boxes):
      while True:
        vals = [common.randint(0, 1) for _ in range(9)]
        if sum(vals) not in [0, 9]: break  # need at least one dot, but not all.
      colors.extend(vals)

  grid, output = common.grids(size, size, 8)
  for row, col in zip(rows, cols):
    common.rect(grid, 5, 5, row, col, 0)
    common.rect(output, 5, 5, row, col, 0)
  order = [1, 7, 6, 4, 0, 5, 2, 9, 3]
  for group in range(len(rows)):
    for r in range(3):
      for c in range(3):
        row = rows[group] + r + 1
        col = cols[group] + c + 1
        color = colors[group * 9 + r * 3 + c]
        output[row][col] = grid[row][col] = 8 * color
        if not color: output[row][col] = order[r * 3 + c]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=12, rows=[1, 7], cols=[1, 4],
               colors=[1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0]),
      generate(size=9, rows=[2], cols=[2], colors=[1, 0, 1, 0, 0, 0, 1, 0, 1]),
      generate(size=13, rows=[0, 6, 7], cols=[8, 7, 0],
               colors=[0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1]),
  ]
  test = [
      generate(size=16, rows=[0, 5, 7, 11], cols=[11, 5, 11, 1],
               colors=[1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0]),
  ]
  return {"train": train, "test": test}

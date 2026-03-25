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


def generate(rows=None, cols=None, heights=None, lefts=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: The rows of the boxes.
    cols: The columns of the boxes.
    heights: The heights of the boxes.
    lefts: The lefts of the boxes.
  """

  if rows is None:
    num_boxes = common.randint(1, 2)
    if num_boxes == 1:
      height = common.randint(3, 5)
      heights = [height]
      rows = [common.randint(1, 10 - height)]
    else:
      while True:
        heights = [common.randint(3, 5) for _ in range(num_boxes)]
        rows = [common.randint(1, 2)]
        rows.append(rows[0] + heights[0] + common.randint(1, 2))
        if rows[-1] + heights[-1] <= 10: break
    cols = [common.randint(1, 5) for _ in range(num_boxes)]
    lefts = [common.randint(0, 1) for _ in range(num_boxes)]

  grid, output = common.grids(10, 10)
  for row, col, height, left in zip(rows, cols, heights, lefts):
    common.hollow_rect(grid, 4, height, row, col, 5)
    common.hollow_rect(output, 4, height, row, col, 5)
    common.hollow_rect(output, 2, height - 2, row + 1, col + 1, 2)
    grid[row][col + left + 1] = 0
    output[row][col + left + 1] = 2
    c = col + left + 1
    while c >= 0 and c < 10:
      output[row - 1][c] = 2
      c += -1 if left else 1
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[3], cols=[3], heights=[5], lefts=[0]),
      generate(rows=[3], cols=[2], heights=[4], lefts=[1]),
      generate(rows=[2, 7], cols=[1, 5], heights=[4, 3], lefts=[0, 1]),
  ]
  test = [
      generate(rows=[1, 7], cols=[1, 5], heights=[4, 3], lefts=[1, 1]),
  ]
  return {"train": train, "test": test}

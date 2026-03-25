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


def generate(wide=None, tall=None, left_padding=None, right_padding=None,
             top_padding=None, bottom_padding=None, missing=None, brows=None,
             bcols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    wide: The # of mega boxes per row.
    tall: The # of mega boxes per column.
    left_padding: The # of pixels to pad on the left.
    right_padding: The # of pixels to pad on the right.
    top_padding: The # of pixels to pad on the top.
    bottom_padding: The # of pixels to pad on the bottom.
    missing: The index of the missing pixel for each box.
    brows: The row offset for each box.
    bcols: The column offset for each box.
  """

  if wide is None:
    orientation = common.randint(0, 1)
    wide, tall = 3 if orientation else 2, 2 if orientation else 3
    left_padding, right_padding = common.randint(0, 2), common.randint(-1, 2)
    top_padding, bottom_padding = common.randint(0, 2), common.randint(-1, 2)
    missing = [common.randint(-1, 3) for _ in range(6)]
    brows = [common.randint(0, 2) for _ in range(6)]
    bcols = [common.randint(0, 2) for _ in range(6)]

  width = 5 * wide + 1 + left_padding + right_padding
  height = 5 * tall + 1 + top_padding + bottom_padding
  grid, output = common.grids(width, height)
  # Draw the red dots.
  for row in range(tall + 1):
    for col in range(wide + 1):
      common.draw(grid, 5 * row + top_padding, 5 * col + left_padding, 2)
      common.draw(output, 5 * row + top_padding, 5 * col + left_padding, 2)
  # Draw the blue shapes.
  for row in range(tall):
    for col in range(wide):
      index = row * wide + col
      brow, bcol = brows[index], bcols[index]
      for r, c in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        if missing[index] == 2 * r + c: continue
        row_offset = top_padding + 5 * row + r + 1
        col_offset = left_padding + 5 * col + c + 1
        grid[row_offset + brow][col_offset + bcol] = 1
        output[row_offset + 1][col_offset + 1] = 1
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(wide=3, tall=2, left_padding=1, right_padding=-1, top_padding=1,
               bottom_padding=2, missing=[-1, 1, 3, 0, 3, 1],
               brows=[0, 2, 0, 2, 1, 1], bcols=[0, 0, 1, 1, 1, 1]),
      generate(wide=3, tall=2, left_padding=2, right_padding=1, top_padding=2,
               bottom_padding=0, missing=[1, 2, 0, 1, -1, 3],
               brows=[0, 1, 0, 2, 0, 1], bcols=[0, 1, 2, 0, 1, 0]),
      generate(wide=2, tall=3, left_padding=0, right_padding=-1, top_padding=1,
               bottom_padding=0, missing=[-1, 1, 3, 1, 0, 3],
               brows=[1, 0, 2, 1, 0, 1], bcols=[0, 1, 0, 1, 2, 1]),
  ]
  test = [
      generate(wide=2, tall=3, left_padding=2, right_padding=0, top_padding=1,
               bottom_padding=0, missing=[-1, 3, -1, 0, 2, 3],
               brows=[2, 2, 2, 0, 1, 0], bcols=[0, 1, 1, 2, 1, 1]),
  ]
  return {"train": train, "test": test}

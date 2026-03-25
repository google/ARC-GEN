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


def generate(width=None, height=None, top=None, bottom=None, rows=None,
             cols=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    top: The top color.
    bottom: The bottom color.
    rows: The rows of the pixels.
    cols: The columns of the pixels.
    xpose: Whether to transpose the grid.
  """

  if width is None:
    width, height = common.randint(8, 16), 2 * common.randint(4, 9)
    colors = common.sample([2, 3, 4, 8], 2)
    top, bottom = colors[0], colors[1]
    num_pixels = width * height // 20 + common.randint(-2, 2)
    while True:
      rows = [common.randint(2, height - 3) for _ in range(num_pixels)]
      cols = [common.randint(0, width - 1) for _ in range(num_pixels)]
      if not common.overlaps(rows, cols, [1] * num_pixels, [1] * num_pixels, 1):
        break
    xpose = common.randint(0, 1)

  grid, output = common.grids(width, height)
  for c in range(width):
    output[0][c] = grid[0][c] = top
    output[height - 1][c] = grid[height - 1][c] = bottom
  for row, col in zip(rows, cols):
    output[row][col] = grid[row][col] = 1
    side = -1 if row < height // 2 else 1
    output[row + side][col] = top if side == -1 else bottom
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=10, height=14, top=2, bottom=4,
               rows=[2, 2, 3, 5, 6, 7, 9, 10, 11],
               cols=[1, 8, 3, 2, 6, 3, 1, 6, 8], xpose=False),
      generate(width=13, height=12, top=8, bottom=3,
               rows=[2, 2, 3, 5, 6, 8, 8, 9], cols=[2, 8, 4, 9, 5, 2, 12, 8],
               xpose=False),
      generate(width=12, height=10, top=3, bottom=4, rows=[2, 2, 3, 5, 6, 6],
               cols=[2, 10, 4, 5, 1, 8], xpose=True),
  ]
  test = [
      generate(width=16, height=18, top=2, bottom=8,
               rows=[2, 3, 4, 4, 6, 8, 10, 10, 11, 14, 15, 15],
               cols=[1, 14, 3, 10, 6, 8, 1, 12, 5, 11, 0, 14], xpose=True),
  ]
  return {"train": train, "test": test}

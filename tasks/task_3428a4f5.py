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


def generate(rows=None, cols=None, width=5, height=6):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    width: the width of the input grid
    height: *half* the height of the input grid
  """
  if rows is None:
    top_pixels = common.random_pixels(width, height)
    bottom_pixels = common.random_pixels(width, height)
    top_rows, top_cols = zip(*top_pixels)
    bottom_rows, bottom_cols = zip(*bottom_pixels)
    bottom_rows = tuple([r + height + 1 for r in bottom_rows])
    rows, cols = top_rows + bottom_rows, top_cols + bottom_cols

  grid = common.grid(width, 2 * height + 1)
  output = common.grid(width, height)
  for c in range(width):
    grid[height][c] = common.yellow()
  for r, c in zip(rows, cols):
    grid[r][c] = common.red()
    r -= 0 if r < height else height + 1
    output[r][c] = (output[r][c] + 1) % 2
  for r in range(height):
    for c in range(width):
      output[r][c] *= common.green()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 1, 2, 2, 2, 3, 3, 3, 4, 5, 7, 8, 8, 9, 9, 10, 11,
                     11, 12, 12],
               cols=[3, 4, 2, 4, 0, 3, 4, 0, 1, 4, 4, 1, 0, 0, 1, 0, 2, 2, 3, 4,
                     0, 3]),
      generate(rows=[0, 0, 0, 0, 1, 2, 2, 2, 2, 3, 3, 4, 4, 4, 4, 5, 5, 5, 8, 9,
                     9, 10, 11, 11, 12, 12, 12],
               cols=[1, 2, 3, 4, 4, 0, 2, 3, 4, 2, 3, 0, 1, 2, 3, 0, 1, 4, 2, 0,
                     4, 3, 1, 3, 1, 2, 3]),
      generate(rows=[0, 0, 0, 0, 1, 1, 1, 1, 2, 3, 3, 4, 4, 4, 4, 5, 5, 7, 7, 7,
                     8, 8, 9, 9, 10, 10, 11, 11, 11, 12, 12, 12],
               cols=[0, 1, 3, 4, 0, 2, 3, 4, 0, 1, 3, 0, 1, 2, 4, 0, 2, 0, 3, 4,
                     2, 4, 0, 1, 2, 4, 1, 3, 4, 1, 2, 4]),
      generate(rows=[0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 4, 5, 5, 5, 7, 7,
                     7, 7, 8, 8, 9, 9, 9, 10, 10, 11, 11, 11, 12, 12, 12],
               cols=[1, 3, 0, 1, 3, 4, 1, 2, 3, 1, 2, 1, 2, 3, 4, 0, 2, 4, 0, 2,
                     3, 4, 1, 2, 0, 2, 4, 0, 4, 0, 1, 3, 0, 2, 3]),
  ]
  test = [
      generate(rows=[0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 5, 5, 5, 5,
                     5, 7, 7, 8, 8, 9, 9, 9, 9, 10, 10, 11, 11, 11, 12, 12, 12,
                     12],
               cols=[0, 2, 3, 0, 3, 4, 0, 1, 2, 0, 1, 2, 3, 4, 1, 2, 0, 1, 2, 3,
                     4, 3, 4, 0, 4, 0, 1, 2, 4, 1, 2, 0, 2, 3, 0, 2, 3, 4]),
      generate(rows=[0, 0, 0, 1, 1, 1, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 5, 7, 7, 8,
                     8, 8, 8, 9, 9, 10, 11, 11, 11, 12],
               cols=[0, 2, 4, 0, 2, 4, 3, 1, 2, 3, 0, 2, 3, 0, 1, 2, 4, 0, 1, 1,
                     2, 3, 4, 2, 3, 1, 1, 2, 4, 0]),
  ]
  return {"train": train, "test": test}

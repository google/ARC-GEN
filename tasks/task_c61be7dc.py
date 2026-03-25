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


def generate(border=None, mid=None, rows=None, cols=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    border: The thickness of the initial border.
    mid: The thickness of the middle section.
    rows: The rows of the grey dots.
    cols: The the columns of the grey dots.
    xpose: Whether to transpose the grid.
  """

  def draw():
    size = 2 * border + mid + 2
    grid, output = common.grids(size, size, 7)
    # Draw the input black lines.
    for r in range(border):
      grid[r][size // 2] = grid[size - r - 1][size // 2] = 0
    for c in range(size):
      grid[border][c] = grid[size - border - 1][c] = 0
    # Draw the output black lines.
    for r in range(size // 2):
      output[r][size // 2] = output[size - r - 1][size // 2] = 0
    for c in range(size):
      output[size // 2 - 1][c] = output[size // 2 + 1][c] = 0
    # Draw the input grey dots.
    for row, col in zip(rows, cols):
      r = border + 1 + row
      grid[r][size // 2 + col] = grid[r][size // 2 - col] = 5
    # Draw the output grey dots.
    num_grey = common.flatten(grid).count(5)
    if num_grey > size: return None, None
    for c in range(num_grey):
      output[size // 2][(size - num_grey) // 2 + c] = 5
    if xpose: grid, output = common.transpose(grid), common.transpose(output)
    return grid, output

  if border is None:
    border, mid = common.randint(1, 5), 2 * common.randint(1, 3) + 1
    xpose = common.randint(0, 1)
    size = 2 * border + mid + 2
    while True:
      rows, cols = [], []
      for r in range(mid):
        col = []
        while not col:
          for c in range(size // 2):
            if common.randint(0, pow(2, c)) == 0: col.append(c)
        rows.extend([r] * len(col))
        cols.extend(col)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(border=3, mid=3, rows=[0, 0, 1, 1, 2, 2],
               cols=[0, 1, 0, 1, 0, 1], xpose=True),
      generate(border=2, mid=3, rows=[0, 1, 2, 2], cols=[0, 0, 0, 1],
               xpose=False),
      generate(border=3, mid=5, rows=[0, 0, 0, 1, 1, 2, 2, 3, 4],
               cols=[0, 1, 2, 0, 1, 0, 1, 0, 0], xpose=True),
  ]
  test = [
      generate(border=5, mid=7, rows=[0, 1, 2, 3, 4, 5, 6, 6],
               cols=[1, 1, 0, 0, 0, 0, 0, 1], xpose=False),
  ]
  return {"train": train, "test": test}

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


def generate(size=None, rows=None, cols=None, color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    rows: The rows of the pixels.
    cols: The columns of the pixels.
    color: The color of the background.
  """

  def draw():
    grid, output = common.grids(size, size, color)
    # Draw centers and borders.
    for row, col in zip(rows, cols):
      grid[row][col] = 1
      output[row][col] = 2
      for r, c in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        common.draw(output, row + r, col + c, 3)
    # Draw blue crossings (but check for clobbering).
    for row, col in zip(rows, cols):
      for r in range(size):
        if r == row: continue
        if output[r][col] in [2, 3]: return None, None
        output[r][col] = 1
      for c in range(size):
        if c == col: continue
        if output[row][c] in [2, 3]: return None, None
        output[row][c] = 1
    return grid, output

  if rows is None:
    size = common.randint(8, 16)
    pixels = (size - 1) // 2 - 2
    color = common.random_color(exclude=[1, 2, 3])
    while True:
      rows = common.sample(range(size), pixels)
      cols = common.sample(range(size), pixels)
      grid, _ = draw()
      if grid is not None: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=9, rows=[3, 6], cols=[3, 6], color=9),
      generate(size=13, rows=[1, 3, 6, 9], cols=[11, 2, 9, 5], color=8),
      generate(size=11, rows=[1, 4, 9], cols=[8, 2, 6], color=7),
  ]
  test = [
      generate(size=14, rows=[2, 5, 11, 13], cols=[7, 2, 4, 13], color=8),
  ]
  return {"train": train, "test": test}

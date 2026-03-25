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


def generate(width=None, height=None, line=None, rows=None, cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    line: The row of the line.
    rows: The rows of the pixels.
    cols: The columns of the pixels.
  """

  def draw():
    bounces = False
    grid, output = common.grids(width, height)
    for c in range(width):
      output[line][c] = grid[line][c] = 2
    for row, col in zip(rows, cols):
      if grid[row][col] != 0: return None, None, None
      grid[row][col] = 4
      bounces = bounces or row + 2 == line
      for c in range(width):
        if row + 2 != line and c != col: continue
        the_row = row + 1 - abs(col - c)
        if common.get_pixel(output, the_row, c) not in [-1, 0]:
          return None, None, None
        common.draw(output, the_row, c, 4)
    return grid, output, bounces

  if width is None:
    width = common.randint(3, 8)
    height = width + common.randint(2, 4)
    line = common.randint(3, height - 1)
    num_pixels = common.randint(1, (width + 1) // 2)
    expected_bounces = True if common.randint(0, 4) else False
    while True:
      rows = common.sample(list(range(height - 1)), num_pixels)
      cols = common.sample(list(range(width)), num_pixels)
      grid, _, bounces = draw()
      if grid and bounces == expected_bounces: break

  grid, output, _ = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=8, height=12, line=9, rows=[0, 1, 4, 7, 10],
               cols=[1, 5, 2, 4, 3]),
      generate(width=6, height=10, line=5, rows=[2, 3], cols=[1, 4]),
      generate(width=3, height=6, line=4, rows=[1], cols=[1]),
      generate(width=5, height=7, line=6, rows=[4], cols=[2]),
  ]
  test = [
      generate(width=8, height=12, line=3, rows=[0, 1, 6], cols=[4, 0, 1]),
  ]
  return {"train": train, "test": test}

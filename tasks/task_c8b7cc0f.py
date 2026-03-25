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


def generate(size=None, rows=None, cols=None, wide=None, tall=None, brow=None,
             bcol=None, color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    rows: The rows of the pixels.
    cols: The columns of the pixels.
    wide: The width of the rectangle.
    tall: The height of the rectangle.
    brow: The row of the rectangle.
    bcol: The column of the rectangle.
    color: The color of the foreground.
  """

  def draw():
    grid, output = common.grid(size, size), common.grid(3, 3)
    for row, col in zip(rows, cols):
      grid[row][col] = color
    common.hollow_rect(grid, wide, tall, brow, bcol, 1)
    count = 0
    for row in range(brow + 1, brow + tall - 1):
      for col in range(bcol + 1, bcol + wide - 1):
        if grid[row][col] == color: count += 1
    if count < 3 or count > 6: return None, None
    for i in range(count):
      output[i // 3][i % 3] = color
    return grid, output

  if size is None:
    size = 7 if common.randint(0, 1) else 9
    color = common.random_color(exclude=[1])
    while True:
      rows, cols = [], []
      for pixel in common.random_pixels(size, size, 0.1):
        rows, cols = rows + [pixel[0]], cols + [pixel[1]]
      wide, tall = common.randint(4, size - 2), common.randint(4, size - 2)
      brow = common.randint(0, size - tall)
      bcol = common.randint(0, size - wide)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=9, rows=[1, 2, 2, 3, 4, 5, 5, 7],
               cols=[2, 4, 6, 5, 7, 1, 4, 3], wide=6, tall=6, brow=1, bcol=3,
               color=6),
      generate(size=7, rows=[1, 1, 2, 3, 4, 5, 5], cols=[1, 5, 2, 6, 4, 1, 3],
               wide=6, tall=4, brow=3, bcol=0, color=4),
      generate(size=9, rows=[0, 1, 2, 3, 4, 5, 6, 7, 7],
               cols=[5, 0, 5, 7, 5, 3, 1, 4, 7], wide=5, tall=8, brow=1, bcol=2,
               color=3),
  ]
  test = [
      generate(size=9, rows=[0, 0, 2, 3, 3, 4, 5, 5, 7, 8],
               cols=[0, 6, 2, 4, 7, 5, 1, 8, 3, 7], wide=7, tall=6, brow=1,
               bcol=0, color=2),
  ]
  return {"train": train, "test": test}

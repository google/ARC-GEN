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
    color: The color of the pixels.
  """

  def draw():
    grid, output = common.grid(size, size), common.grid(2 * size, 2 * size)
    for row, col in zip(rows, cols):
      grid[row][col] = color
      for r in range(2 * size):
        if common.get_pixel(output, r, r - 2 * (row - col)) not in [-1, 0]:
          return None, None
        common.draw(output, r, r - 2 * (row - col), 1)
      for r, c in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        output[2 * row + r][2 * col + c] = color
    return grid, output

  if size is None:
    size, color = common.randint(2, 6), common.random_color(exclude=[1])
    while True:
      row, rows = 0, []
      while row < size:
        rows.append(row)
        row += common.randint(1, 3)
      cols = [common.randint(0, size - 1) for _ in rows]
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=2, rows=[0], cols=[0], color=2),
      generate(size=5, rows=[0, 1, 3], cols=[3, 1, 1], color=5),
      generate(size=6, rows=[0, 2], cols=[5, 1], color=3),
  ]
  test = [
      generate(size=3, rows=[0, 2], cols=[1, 0], color=4),
  ]
  return {"train": train, "test": test}

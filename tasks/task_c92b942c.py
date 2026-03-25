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


def generate(width=None, height=None, color=None, rows=None, cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the input grid.
    height: The height of the input grid.
    color: The color of the pixels.
    rows: The rows of the pixels.
    cols: The columns of the pixels.
  """

  def draw():
    grid = common.grid(width, height)
    output = common.grid(3 * width, 3 * height)
    for row in rows:
      for r in range(3):
        for c in range(3 * width):
          output[r * height + row][c] = 1
    for row, col in zip(rows, cols):
      grid[row][col] = color
      for r in range(3):
        for c in range(3):
          rr, cc = r * height + row - 1, c * width + col - 1
          if common.get_pixel(output, rr, cc) not in [-1, 0, 3]:
            return None, None
          common.draw(output, rr, cc, 3)
          rr, cc = r * height + row, c * width + col
          if output[rr][cc] not in [-1, 0, 1]: return None, None
          output[rr][cc] = color
          rr, cc = r * height + row + 1, c * width + col + 1
          if common.get_pixel(output, rr, cc) not in [-1, 0, 3]:
            return None, None
          common.draw(output, rr, cc, 3)
    return grid, output

  if width is None:
    width, height = common.randint(3, 6), common.randint(3, 6)
    color = common.random_color(exclude=[1, 3])
    while True:
      points = common.randint(1, 3)
      rows = [common.randint(0, height - 1) for _ in range(points)]
      cols = [common.randint(0, width - 1) for _ in range(points)]
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=6, height=4, color=4, rows=[1, 3, 3], cols=[2, 0, 4]),
      generate(width=4, height=2, color=5, rows=[0], cols=[2]),
      generate(width=5, height=5, color=2, rows=[2], cols=[2]),
      generate(width=3, height=3, color=6, rows=[1], cols=[1]),
  ]
  test = [
      generate(width=3, height=3, color=2, rows=[0], cols=[0]),
  ]
  return {"train": train, "test": test}

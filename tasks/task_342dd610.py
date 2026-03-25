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


def generate(size=None, rows=None, cols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    rows: The rows of the pixels.
    cols: The columns of the pixels.
    colors: The colors of the pixels.
  """

  def draw():
    grid, output = common.grids(size, size, 8)
    for row, col, color in zip(rows, cols, colors):
      r, c = row, col
      grid[r][c] = color
      if color == 1: r, c = r + 0, c + 1
      if color == 2: r, c = r + 0, c - 2
      if color == 7: r, c = r - 2, c + 0
      if color == 9: r, c = r + 2, c + 0
      if r < 0 or c < 0 or r >= size or c >= size: return None, None
      if output[r][c] != 8: return None, None
      output[r][c] = color
    return grid, output

  if size is None:
    size = 2 * common.randint(5, 8)
    dots = size - common.randint(6, 9)
    while True:
      rows = [common.randint(0, size - 1) for _ in range(dots)]
      cols = [common.randint(0, size - 1) for _ in range(dots)]
      colors = common.choices([1, 2, 7, 9], dots)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=10, rows=[4, 6], cols=[4, 8], colors=[7, 7]),
      generate(size=10, rows=[5, 9], cols=[7, 7], colors=[2, 2]),
      generate(size=10, rows=[4], cols=[2], colors=[9]),
      generate(size=10, rows=[5, 9], cols=[7, 7], colors=[1, 1]),
  ]
  test = [
      generate(size=16, rows=[1, 2, 3, 4, 7, 8, 10, 11, 12, 13],
               cols=[7, 2, 13, 8, 1, 8, 10, 2, 11, 5],
               colors=[9, 1, 2, 7, 9, 2, 1, 2, 9, 7]),
  ]
  return {"train": train, "test": test}

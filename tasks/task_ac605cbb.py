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

  def draw(must_join=False):
    grid, output = common.grids(size, size)
    joins, bad = [], False
    def put(pixels, color):
      nonlocal joins, bad
      for pixel in pixels:
        r, c = pixel
        if r < 0 or c < 0 or r >= size or c >= size:
          bad = True  # out of bounds
          break
        if color == 5 and output[r][c] not in [0, 5]:
          bad = True  # grays can only be placed on blacks or grays
          break
        if color != 5 and output[r][c] not in [0]:
          bad = True  # non-gray should never touch anything
          break
        if output[r][c] == 5: joins.append((r, c))
        output[r][c] = color
    for row, col, color in zip(rows, cols, colors):
      grid[row][col] = color
      put([(row, col)], color)
      if color == 1:
        put([(row, col + 1), (row, col + 2)], 5)
        put([(row - 1, col + 2)], 1)
      if color == 2:
        put([(row, col - 1), (row, col - 2), (row, col - 3)], 5)
        put([(row, col - 4)], 2)
      if color == 3:
        put([(row + 1, col), (row + 2, col)], 5)
        put([(row + 3, col)], 3)
      if color == 6:
        put([(row - 1, col), (row - 2, col), (row - 3, col), (row - 4, col), (row - 5, col)], 5)
        put([(row - 6, col)], 6)
    if must_join and not joins: bad = True
    if len(joins) > 1: bad = True  # test & training have at most 1 join
    for pixel in joins:
      r, c = pixel
      while r < size and c >= 0:
        if r != pixel[0] and c != pixel[1] and output[r][c] != 0: bad = True
        output[r][c] = 4
        r, c = r + 1, c - 1
    if bad: return None, None
    return grid, output

  if size is None:
    size = common.randint(9, 11)
    must_join = common.randint(0, 1)  # about half of problems should have joins
    while True:
      num_pixels = common.randint(1, 4)
      colors = common.sample([1, 2, 3, 6], num_pixels)
      rows = [common.randint(0, size - 1) for _ in range(num_pixels)]
      cols = [common.randint(0, size - 1) for _ in range(num_pixels)]
      grid, _ = draw(must_join)
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=11, rows=[4, 6, 9], cols=[5, 3, 7], colors=[2, 6, 1]),
      generate(size=10, rows=[2, 5], cols=[3, 6], colors=[3, 1]),
      generate(size=10, rows=[2, 4], cols=[4, 6], colors=[3, 2]),
      generate(size=11, rows=[2, 4, 5], cols=[3, 5, 7], colors=[1, 2, 3]),
      generate(size=10, rows=[4, 7], cols=[3, 5], colors=[1, 2]),
      generate(size=9, rows=[7], cols=[3], colors=[6]),
  ]
  test = [
      generate(size=11, rows=[2, 6, 7, 7], cols=[1, 7, 5, 9], colors=[1, 2, 6, 3]),
  ]
  return {"train": train, "test": test}

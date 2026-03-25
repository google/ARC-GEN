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


def generate(size=None, color=None, rows=None, cols=None, lengths=None,
             cdirs=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    color: The color of the lines.
    rows: The rows of the lines.
    cols: The columns of the lines.
    lengths: The lengths of the lines.
    cdirs: The directions of the lines.
  """

  def draw():
    if lengths.count(0) > 1: return None, None
    grid, output = common.grids(size, size, 7)
    for row, col, length, cdir in zip(rows, cols, lengths, cdirs):
      # First, check that there's room around the line.
      for i in range(-length, length + 1):
        for j in [-1, 0, 1]:
          r = (row + i) if cdir else (row + j)
          c = (col + j) if cdir else (col + i)
          if common.get_pixel(grid, r, c) not in [-1, 7]: return None, None
      r = (row - length - 1) if cdir else row
      c = col if cdir else (col - length - 1)
      if common.get_pixel(grid, r, c) not in [-1, 7]: return None, None
      r = (row + length + 1) if cdir else row
      c = col if cdir else (col + length + 1)
      if common.get_pixel(grid, r, c) not in [-1, 7]: return None, None
      # Second, draw the line.
      for i in range(-length, length + 1):
        r = (row + i) if cdir else row
        c = col if cdir else (col + i)
        if grid[r][c] != 7: return None, None
        grid[r][c] = color
        r = (row + i) if not cdir else row
        c = col if not cdir else (col + i)
        if output[r][c] != 7: return None, None
        output[r][c] = color
    return grid, output

  if size is None:
    size = 2 * common.randint(3, 6) + 1
    color = common.random_color(exclude=[7])
    num_lines = size - 4
    while True:
      lengths = [common.randint(0, size // 2 - 1) for _ in range(num_lines)]
      cdirs = [common.randint(0, 1) for _ in range(num_lines)]
      rows = [common.randint(length, size - 1 - length) for length in lengths]
      cols = [common.randint(length, size - 1 - length) for length in lengths]
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=9, color=5, rows=[1, 1, 3, 5, 6], cols=[1, 5, 3, 6, 2],
               lengths=[1, 0, 1, 2, 2], cdirs=[1, 1, 1, 1, 0]),
      generate(size=9, color=2, rows=[1, 2, 4, 6, 7], cols=[3, 6, 2, 6, 2],
               lengths=[1, 1, 1, 1, 1], cdirs=[0, 1, 1, 0, 0]),
      generate(size=11, color=8, rows=[2, 3, 3, 5, 7, 8, 9],
               cols=[7, 1, 3, 9, 6, 2, 9], lengths=[2, 1, 0, 1, 3, 2, 1],
               cdirs=[0, 1, 1, 0, 1, 0, 0]),
  ]
  test = [
      generate(size=13, color=9, rows=[2, 2, 4, 5, 7, 7, 10, 10, 11, 11],
               cols=[2, 9, 11, 4, 6, 9, 1, 4, 8, 11],
               lengths=[2, 2, 1, 4, 0, 1, 1, 2, 1, 1],
               cdirs=[0, 0, 0, 0, 1, 1, 0, 1, 1, 0]),
  ]
  return {"train": train, "test": test}

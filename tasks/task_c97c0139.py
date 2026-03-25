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


def generate(width=None, height=None, rows=None, cols=None, wides=None,
             talls=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: width of the grid.
    height: height of the grid.
    rows: rows of the lines.
    cols: cols of the lines.
    wides: wides of the lines.
    talls: talls of the lines.
  """

  if width is None:
    width, height = common.randint(18, 22), common.randint(18, 22)
    num_lines = common.randint(1, 3)
    while True:
      sizes = [common.randint(5, 14) for _ in range(num_lines)]
      rs = [common.randint(1, height - s - 1) for s in sizes]
      cs = [common.randint(1, width - s - 1) for s in sizes]
      if not common.overlaps(rs, cs, sizes, sizes, 1): break
    rows, cols, wides, talls = [], [], [], []
    for size, r, c in zip(sizes, rs, cs):
      if common.randint(0, 1):
        rows.append(r)
        cols.append(c + size // 2)
        wides.append(0)
        talls.append(size)
      else:
        rows.append(r + size // 2)
        cols.append(c)
        wides.append(size)
        talls.append(0)

  grid, output = common.grids(width, height)
  for row, col, wide, tall in zip(rows, cols, wides, talls):
    if wide > 0:
      for c in range(wide):
        grid[row][col + c] = output[row][col + c] = 2
      for r in range(1, wide):
        for c in range(r, wide - r):
          output[row - r][col + c] = output[row + r][col + c] = 8
    if tall > 0:
      for r in range(tall):
        grid[row + r][col] = output[row + r][col] = 2
      for c in range(1, tall):
        for r in range(c, tall - c):
          output[row + r][col - c] = output[row + r][col + c] = 8
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=21, height=19, rows=[2, 12], cols=[4, 9], wides=[0, 9], talls=[5, 0]),
      generate(width=19, height=17, rows=[7], cols=[2], wides=[14], talls=[0]),
  ]
  test = [
      generate(width=22, height=21, rows=[4, 9, 11], cols=[2, 11, 5], wides=[6, 10, 0], talls=[0, 0, 7]),
  ]
  return {"train": train, "test": test}

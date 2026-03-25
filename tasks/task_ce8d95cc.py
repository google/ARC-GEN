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


def generate(width=None, height=None, cdirs=None, vals=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    cdirs: The directions of the lines.
    vals: The row or col values of the lines.
    colors: The colors of the lines.
  """

  if width is None:
    width, height = common.randint(8, 13), common.randint(8, 13)
    while True:
      cdirs, vals = [], []
      row = common.randint(1, 4)
      while row + 1 < height:
        cdirs.append(1)
        vals.append(row)
        row += common.randint(2, 5)
      col = common.randint(1, 4)
      while col + 1 < width:
        cdirs.append(0)
        vals.append(col)
        col += common.randint(2, 5)
      if len(cdirs) <= 9: break
    order = common.shuffle(range(len(cdirs)))
    cdirs = [cdirs[i] for i in order]
    vals = [vals[i] for i in order]
    colors = common.random_colors(len(cdirs))

  grid, output = common.grids(width, height)
  for cdir, val, color in zip(cdirs, vals, colors):
    if cdir:
      for r in range(height):
        output[r][val] = grid[r][val] = color
    else:
      for c in range(width):
        output[val][c] = grid[val][c] = color
  i = 1
  while i < len(output):
    if output[i] == output[i - 1]: output.pop(i)
    else: i += 1
  i = 1
  while i < len(output[0]):
    col_next = [output[r][i] for r in range(len(output))]
    col_prev = [output[r][i - 1] for r in range(len(output))]
    if col_next == col_prev:
      for r in range(len(output)):
        output[r].pop(i)
    else:
      i += 1
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=9, height=12, cdirs=[0, 1, 0], vals=[4, 2, 9], colors=[3, 4, 8]),
      generate(width=11, height=12, cdirs=[0, 0, 1, 1, 1], vals=[3, 9, 2, 5, 7], colors=[2, 5, 1, 8, 3]),
      generate(width=11, height=12, cdirs=[0, 1, 0, 1, 0], vals=[1, 2, 6, 7, 10], colors=[7, 3, 2, 1, 8]),
      generate(width=11, height=10, cdirs=[0, 0, 1, 1], vals=[1, 6, 3, 8], colors=[3, 5, 8, 6]),
  ]
  test = [
      generate(width=13, height=12, cdirs=[1, 0, 0, 1, 0, 1, 1], vals=[2, 3, 6, 5, 9, 7, 10], colors=[3, 6, 1, 2, 8, 7, 4]),
  ]
  return {"train": train, "test": test}

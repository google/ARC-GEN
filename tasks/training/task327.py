# Copyright 2025 Google LLC
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


def generate(rows=None, cols=None, colors=None, size=3):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: digits representing colors to be used
    size: the width and height of the (square) grid
  """
  if rows is None:
    rows, cols, diags = [], [], []
    for (r, c) in common.shuffle(common.all_pixels(size, size)):
      diag = c - r
      if diag in diags: continue
      diags.append(diag)
      rows.append(r)
      cols.append(c)
    colors = common.random_colors(3)

  grid, output = common.grid(size, size), common.grid(2 * size, 2 * size)
  for r, c, color in zip(rows, cols, colors):
    grid[r][c] = color
    for idx in range(2 * size - max(r, c)):
      output[r + idx][c + idx] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1], cols=[0, 1, 0], colors=[6, 1, 3]),
      generate(rows=[0, 1, 2], cols=[1, 1, 0], colors=[4, 8, 2]),
      generate(rows=[0, 1, 1], cols=[2, 0, 1], colors=[6, 1, 3]),
  ]
  test = [
      generate(rows=[0, 2, 2], cols=[2, 1, 2], colors=[3, 4, 9]),
  ]
  return {"train": train, "test": test}

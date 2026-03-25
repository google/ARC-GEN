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


def generate(prows=None, pcols=None, colors=None, size=15):
  """Returns input and output grids according to the given parameters.

  Args:
    prows: The rows of the pixels.
    pcols: The columns of the pixels.
    colors: The colors of the pixels.
    size: The size of the grid.
  """

  if prows is None:
    colors = common.random_colors(common.randint(3, 4))
    while True:
      prows = sorted(common.sample(range(1, size - 1), len(colors)))
      pcols = common.sample(range(3, size - 3), len(colors))
      diffs = [prows[i + 1] - prows[i] for i in range(len(colors) - 1)]
      if min(diffs) > 1: break

  grid, output = common.grids(15, 15)
  for i, (prow, pcol, color) in enumerate(zip(prows, pcols, colors)):
    grid[prow][pcol] = color
    for c in range(size):
      output[prow][c] = color
    lb_row = 0 if i == 0 else (prow - (prow - prows[i - 1] - 1) // 2)
    ub_row = size if i + 1 == len(prows) else (prow + (prows[i + 1] - prow + 2) // 2)
    for row in range(lb_row, ub_row):
      output[row][0] = output[row][size - 1] = color
  for c in range(size):
    output[0][c] = colors[0]
    output[size - 1][c] = colors[-1]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(prows=[3, 7, 12], pcols=[6, 8, 3], colors=[2, 7, 8]),
      generate(prows=[1, 3, 7, 9], pcols=[6, 10, 3, 5], colors=[8, 1, 2, 3]),
      generate(prows=[2, 7, 9], pcols=[3, 7, 4], colors=[3, 2, 9]),
      generate(prows=[2, 4, 11], pcols=[10, 4, 7], colors=[6, 2, 8]),
  ]
  test = [
      generate(prows=[2, 4, 9, 12], pcols=[3, 6, 11, 9], colors=[8, 2, 1, 3]),
  ]
  return {"train": train, "test": test}

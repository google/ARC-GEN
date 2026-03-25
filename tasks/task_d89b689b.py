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


def generate(rows=None, cols=None, colors=None, brow=None, bcol=None, size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    brow: the vertical coordinate of the box
    bcol: the horizontal coordinate of the box
    size: the width and height of the (square) grid
  """
  if rows is None:
    brow, bcol = common.randint(2, size - 3), common.randint(2, size - 3)
    rows, cols, colors = [], [], common.random_colors(4,
                                                      exclude=[common.cyan()])
    rows += [common.randint(0, brow - 1)]
    rows += [common.randint(0, brow - 1)]
    rows += [common.randint(brow + 2, size - 1)]
    rows += [common.randint(brow + 2, size - 1)]
    cols += [common.randint(0, bcol - 1)]
    cols += [common.randint(bcol + 2, size - 1)]
    cols += [common.randint(0, bcol - 1)]
    cols += [common.randint(bcol + 2, size - 1)]

  grid, output = common.grids(size, size)
  for r, c, color in zip(rows, cols, colors):
    grid[r][c] = color
  grid[brow][bcol] = grid[brow][bcol + 1] = common.cyan()
  grid[brow + 1][bcol] = grid[brow + 1][bcol + 1] = common.cyan()
  output[brow][bcol] = colors[0]
  output[brow][bcol + 1] = colors[1]
  output[brow + 1][bcol] = colors[2]
  output[brow + 1][bcol + 1] = colors[3]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[3, 0, 8, 9], cols=[1, 8, 1, 9], colors=[6, 7, 4, 9],
               brow=4, bcol=4),
      generate(rows=[0, 1, 8, 6], cols=[2, 8, 1, 9], colors=[5, 9, 2, 1],
               brow=4, bcol=4),
      generate(rows=[0, 0, 7, 6], cols=[3, 9, 2, 9], colors=[1, 4, 3, 6],
               brow=2, bcol=5),
  ]
  test = [
      generate(rows=[3, 1, 9, 8], cols=[1, 6, 2, 8], colors=[3, 4, 6, 7],
               brow=4, bcol=4),
  ]
  return {"train": train, "test": test}

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


def generate(size=None, row=None, col=None, linecolor=None, dotcolor=None,
             b=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the "mini" grid
    row: a vertical coordinate where the odd pixel is placed
    col: a horizontal coordinate where the odd pixel is placed
    linecolor: a digit representing a color to be used for the lines
    dotcolor: a digit representing a color to be used for the dot
    b: the integer used for all background cells
  """
  if size is None:
    size = common.randint(1, 7)
    row, col = common.randint(0, size - 1), common.randint(0, size - 1)
    row += 0 if common.randint(0, 1) == 0 else size + 1
    col += 0 if common.randint(0, 1) == 0 else size + 1
    colors = common.sample(range(10), k=3)
    linecolor, dotcolor, b = colors[0], colors[1], colors[2]

  grid = common.grid(2 * size + 1, 2 * size + 1, b)
  output = common.grid(size, size, b)
  for i in range(2 * size + 1):
    grid[size][i] = grid[i][size] = linecolor
  grid[row][col] = dotcolor
  row -= 0 if row < size else size + 1
  col -= 0 if col < size else size + 1
  output[row][col] = dotcolor
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=2, row=4, col=0, linecolor=3, dotcolor=4, b=8),
      generate(size=3, row=1, col=5, linecolor=2, dotcolor=1, b=4),
      generate(size=5, row=2, col=1, linecolor=1, dotcolor=8, b=3),
  ]
  test = [
      generate(size=6, row=3, col=8, linecolor=0, dotcolor=2, b=1),
  ]
  return {"train": train, "test": test}

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


def generate(size=None, row=None, col=None, color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    row: a vertical coordinate where the pixel should be placed
    col: a horizontal coordinate where the pixel should be placed
    color: a digit representing a color to be used
  """
  if size is None:
    size = common.randint(3, 15)
    row, col = common.randint(0, size - 2), common.randint(0, size - 1)
    color = common.random_color(exclude=[common.yellow()])

  grid, output = common.grids(size, size)
  output[row + 1][col] = grid[row][col] = color
  for r in range(row + 1):
    for c in range(col % 2, size, 2):
      output[r][c] = common.yellow()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=3, row=0, col=1, color=2),
      generate(size=5, row=2, col=2, color=6),
      generate(size=9, row=4, col=2, color=9),
  ]
  test = [
      generate(size=12, row=3, col=5, color=3),
  ]
  return {"train": train, "test": test}

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
    row: an integer with the pixel's row
    col: an integer with the pixel's column
    color: a digit representing the color of the pixel
  """
  if size is None:
    size = 2 * common.randint(2, 10) + 1
    row = common.randint(1, size - 2)
    col = common.randint(1, size - 2)
    color = common.random_color()

  grid, output = common.grids(size, size)
  output[row][col] = grid[row][col] = color
  for c in range(size):
    for r in range(size):
      if r + c != row + col and r - c != row - col: continue
      output[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=15, row=3, col=3, color=2),
      generate(size=15, row=5, col=11, color=7),
      generate(size=7, row=3, col=2, color=8),
  ]
  test = [
      generate(size=17, row=7, col=12, color=6),
  ]
  return {"train": train, "test": test}

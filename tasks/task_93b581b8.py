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


def generate(row=None, col=None, colors=None, size=6):
  """Returns input and output grids according to the given parameters.

  Args:
    row: a vertical coordinate where the center should be placed
    col: a horizontal coordinate where the center should be placed
    colors: a list of four digits representing the colors to be used
    size: the width and height of the (square) grid
  """
  if row is None:
    row, col = common.randint(1, size - 3), common.randint(1, size - 3)
    colors = common.random_colors(4)

  grid, output = common.grids(size, size)
  for r, c, color in zip([0, 0, 1, 1], [0, 1, 0, 1], colors):
    output[row + r][col + c] = grid[row + r][col + c] = color
  for r, c, color in zip([2, 2, -2, -2], [2, -2, 2, -2], colors):
    for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
      common.draw(output, row + r + dr, col + c + dc, color)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(row=2, col=2, colors=[9, 3, 7, 8]),
      generate(row=1, col=1, colors=[4, 6, 2, 1]),
      generate(row=2, col=2, colors=[3, 6, 5, 2]),
  ]
  test = [
      generate(row=3, col=2, colors=[3, 1, 2, 5]),
  ]
  return {"train": train, "test": test}

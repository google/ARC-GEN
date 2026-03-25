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


def generate(row=None, col=None, colors=None, size=8, minisize=5):
  """Returns input and output grids according to the given parameters.

  Args:
    row: a vertical coordinate for the cutout
    col: a horizontal coordinate for the cutout
    colors: a list of colors to be used
    size: the width and height of one quarter of the grid
    minisize: the width and height of the cutout
  """
  if row is None:
    # TODO: Make sure we don't cut out the center.
    row = common.randint(0, size - minisize)
    col = common.randint(0, size - minisize)
    bitmap = common.grid(size, size, common.green())
    for j in range(size):
      for i in range(j + 1):
        color = common.random_color(exclude=[common.green()])
        bitmap[i][j] = bitmap[j][i] = color
    colors = []
    for r in bitmap:
      colors.extend(r)

  grid = common.grid(2 * size, 2 * size, common.green())
  output = common.grid(minisize, minisize, common.green())
  for r in range(size):
    for c in range(size):
      color = colors[r * size + c]
      grid[r][c] = grid[2 * size - r - 1][2 * size - c - 1] = color
      grid[r][2 * size - c - 1] = grid[2 * size - r - 1][c] = color
  for r in range(minisize):
    for c in range(minisize):
      output[r][c] = grid[row + r][col + c]
      grid[row + r][col + c] = common.green()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(row=5, col=9,
               colors=[2, 1, 2, 2, 6, 5, 5, 6, 1, 6, 6, 1, 5, 6, 5, 2, 2, 6, 1,
                       6, 5, 5, 5, 2, 2, 1, 6, 6, 6, 2, 2, 2, 6, 5, 5, 6, 5, 8,
                       5, 7, 5, 6, 5, 2, 8, 8, 5, 8, 5, 5, 5, 2, 5, 5, 5, 8, 6,
                       2, 2, 2, 7, 8, 8, 8]),
      generate(row=0, col=3,
               colors=[8, 9, 9, 8, 7, 7, 2, 2, 9, 8, 9, 9, 7, 1, 7, 2, 9, 9, 8,
                       2, 2, 7, 2, 7, 8, 9, 2, 9, 2, 2, 7, 1, 7, 7, 2, 2, 2, 7,
                       8, 7, 7, 1, 7, 2, 7, 2, 7, 7, 2, 7, 2, 7, 8, 7, 2, 8, 2,
                       2, 7, 1, 7, 7, 8, 2]),
      generate(row=0, col=7,
               colors=[2, 2, 5, 2, 9, 9, 9, 5, 2, 5, 4, 4, 9, 5, 2, 9, 5, 4, 5,
                       4, 9, 2, 5, 5, 2, 4, 4, 4, 5, 9, 5, 2, 9, 9, 9, 5, 9, 6,
                       9, 9, 9, 5, 2, 9, 6, 6, 9, 9, 9, 2, 5, 5, 9, 9, 7, 9, 5,
                       9, 5, 2, 9, 9, 9, 6]),
  ]
  test = [
      generate(row=4, col=8,
               colors=[5, 5, 2, 5, 2, 5, 5, 5, 5, 2, 2, 5, 5, 5, 2, 2, 2, 2, 5,
                       8, 5, 2, 2, 5, 5, 5, 8, 5, 5, 2, 5, 5, 2, 5, 5, 5, 4, 6,
                       6, 9, 5, 5, 2, 2, 6, 6, 9, 9, 5, 2, 2, 5, 6, 9, 6, 9, 5,
                       2, 5, 5, 9, 9, 9, 9]),
  ]
  return {"train": train, "test": test}

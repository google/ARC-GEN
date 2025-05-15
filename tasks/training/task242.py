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


def generate(row=None, col=None, colors=None, size=8, minisize=3):
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
    bitmap = common.grid(size, size)
    for j in range(size):
      for i in range(j + 1):
        bitmap[i][j] = bitmap[j][i] = common.random_color()
    colors = []
    for r in bitmap:
      colors.extend(r)

  grid = common.grid(2 * size, 2 * size)
  output = common.grid(minisize, minisize)
  for r in range(size):
    for c in range(size):
      color = colors[r * size + c]
      grid[r][c] = grid[2 * size - r - 1][2 * size - c - 1] = color
      grid[r][2 * size - c - 1] = grid[2 * size - r - 1][c] = color
  for r in range(minisize):
    for c in range(minisize):
      output[r][c] = grid[row + r][col + c]
      grid[row + r][col + c] = common.black()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(row=5, col=4,
               colors=[2, 1, 3, 5, 1, 1, 1, 8, 1, 2, 5, 7, 1, 7, 8, 8, 3, 5, 4,
                       4, 1, 8, 2, 9, 5, 7, 4, 4, 8, 8, 9, 2, 1, 1, 1, 8, 4, 4,
                       1, 1, 1, 7, 8, 8, 4, 7, 1, 9, 1, 8, 2, 9, 1, 1, 1, 3, 8,
                       8, 9, 2, 1, 9, 3, 1]),
      generate(row=8, col=4,
               colors=[3, 3, 3, 1, 7, 7, 6, 6, 3, 3, 1, 3, 7, 7, 6, 1, 3, 1, 8,
                       8, 6, 6, 9, 7, 1, 3, 8, 5, 6, 1, 7, 9, 7, 7, 6, 6, 3, 3,
                       5, 1, 7, 7, 6, 1, 3, 3, 1, 1, 6, 6, 9, 7, 5, 1, 6, 1, 6,
                       1, 7, 9, 1, 1, 1, 4]),
      generate(row=7, col=10,
               colors=[9, 3, 5, 3, 3, 9, 5, 5, 3, 9, 3, 6, 9, 5, 5, 8, 5, 3, 3,
                       3, 5, 5, 6, 6, 3, 6, 3, 6, 5, 8, 6, 6, 3, 9, 5, 5, 5, 5,
                       2, 1, 9, 5, 5, 8, 5, 8, 1, 6, 5, 5, 6, 6, 2, 1, 9, 3, 5,
                       8, 6, 6, 1, 6, 3, 9]),
  ]
  test = [
      generate(row=5, col=1,
               colors=[4, 8, 9, 9, 6, 6, 5, 1, 8, 6, 9, 9, 6, 7, 1, 5, 9, 9, 5,
                       2, 5, 1, 5, 5, 9, 9, 2, 2, 1, 5, 5, 9, 6, 6, 5, 1, 1, 4,
                       5, 2, 6, 7, 1, 5, 4, 4, 2, 7, 5, 1, 5, 5, 5, 2, 9, 5, 1,
                       5, 5, 9, 2, 7, 5, 9]),
  ]
  return {"train": train, "test": test}

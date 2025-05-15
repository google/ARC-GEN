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


def generate(rows=None, cols=None, row=None, col=None, color=None, size=8,
             minisize=3):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    row: a vertical coordinate where the sprite should be placed
    col: a horizontal coordinate where the sprite should be placed
    color: a digit representing a color to be used
    size: the width and height of the (square) grid
    minisize: the width and height of the sprite
  """
  if rows is None:
    while True:
      rows, cols = common.conway_sprite()
      if common.diagonally_connected(list(zip(rows, cols))): break
    row = common.randint(0, size - minisize - 1)
    col = common.randint(0, size - minisize - 1)
    color = common.random_color()

  grid, output = common.grid(size, size), common.grid(2 * minisize, minisize)
  for r, c in zip(rows, cols):
    grid[row + r][col + c] = color
    output[r][c + minisize] = output[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 2, 2, 2], cols=[0, 1, 1, 0, 1, 2], row=1, col=1,
               color=8),
      generate(rows=[0, 1, 1, 1, 2, 2], cols=[1, 0, 1, 2, 0, 1], row=5, col=2,
               color=2),
      generate(rows=[0, 0, 1, 2], cols=[1, 2, 0, 1], row=1, col=4,
               color=1),
  ]
  test = [
      generate(rows=[0, 1, 1, 1, 2], cols=[2, 0, 1, 2, 0], row=4, col=1,
               color=3),
  ]
  return {"train": train, "test": test}

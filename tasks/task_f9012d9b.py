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


def generate(size=None, minisize=None, colors=None, row=None, col=None,
             bitesize=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    minisize: the width and height of the pattern
    colors: a list of colors to be used
    row: the vertical coordinate where the bite should be placed
    col: the horizontal coordinate where the bite should be placed
    bitesize: the width and height of the bite
  """
  if size is None:
    size = common.randint(4, 7)
    minisize = 2 if size < 7 else 3
    color_list = common.random_colors(2)
    colors = [color_list[common.randint(0, 1)] for _ in range(size * size)]
    bitesize = 1
    if size > 4: bitesize = 2
    if size > 6: bitesize = common.randint(2, 3)
    row = common.randint(0, size - bitesize)
    col = common.randint(0, size - bitesize)

  grid, output = common.grid(size, size), common.grid(bitesize, bitesize)
  for r in range(size):
    for c in range(size):
      mr, mc = r % minisize, c % minisize
      grid[r][c] = colors[mr * minisize + mc]
  for r in range(bitesize):
    for c in range(bitesize):
      output[r][c] = grid[r + row][c + col]
      grid[r + row][c + col] = common.black()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=5, minisize=2, colors=[2, 1, 1, 1], row=3, col=0,
               bitesize=2),
      generate(size=4, minisize=2, colors=[8, 6, 6, 8], row=0, col=2,
               bitesize=1),
      generate(size=7, minisize=3, colors=[2, 2, 5, 2, 2, 5, 5, 5, 5], row=5,
               col=5, bitesize=2),
  ]
  test = [
      generate(size=7, minisize=3, colors=[8, 1, 8, 1, 8, 8, 8, 8, 1], row=0,
               col=4, bitesize=3),
  ]
  return {"train": train, "test": test}

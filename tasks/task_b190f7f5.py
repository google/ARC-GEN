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


def generate(size=None, rows=None, cols=None, colors=None, plusrows=None,
             pluscols=None, pairwise=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    plusrows: a list of vertical coordinates where "plusses" should be placed
    pluscols: a list of horizontal coordinates where "plusses" should be placed
    pairwise: how to orient the two pairs of grids
  """
  if size is None:
    size, pairwise = common.randint(3, 4), common.randint(0, 3)
    num_pixels = common.randint(size * size // 3, 2 * size * size // 3)
    while True:
      pixels = common.sample(common.all_pixels(size, size), num_pixels)
      if common.diagonally_connected(pixels): break
    rows, cols = zip(*pixels)
    color_list = common.sample([1, 2, 3, 4], common.randint(2, 3))
    while True:
      colors = [common.choice(color_list) for _ in pixels]
      if len(set(colors)) > 1: break
    num_plusses = common.randint(size * size // 3, 2 * size * size // 3)
    plusses = common.sample(common.all_pixels(size, size), num_plusses)
    plusrows, pluscols = zip(*plusses)

  width = size * (2 if pairwise in [0, 2] else 1)
  height = size * (2 if pairwise in [1, 3] else 1)
  grid = common.grid(width, height)
  output = common.grid(size * size, size * size)
  rowoffset = size if pairwise == 3 else 0
  coloffset = size if pairwise == 2 else 0
  for row, col, color in zip(rows, cols, colors):
    grid[row + rowoffset][col + coloffset] = color
  rowoffset = size if pairwise == 1 else 0
  coloffset = size if pairwise == 0 else 0
  for row, col in zip(plusrows, pluscols):
    grid[row + rowoffset][col + coloffset] = common.cyan()
  for row, col, color in zip(rows, cols, colors):
    for r, c in zip(plusrows, pluscols):
      output[row * size + r][col * size + c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=3, rows=[0, 0, 1], cols=[0, 2, 1], colors=[2, 4, 3],
               plusrows=[0, 1, 1, 1, 2], pluscols=[1, 0, 1, 2, 1], pairwise=0),
      generate(size=3, rows=[0, 1, 1, 1, 2], cols=[1, 0, 1, 2, 1],
               colors=[4, 1, 2, 4, 1], plusrows=[0, 1, 2, 2],
               pluscols=[2, 0, 0, 1], pairwise=2),
      generate(size=4, rows=[0, 0, 1, 1, 2, 2, 3, 3],
               cols=[0, 3, 1, 2, 1, 2, 0, 3], colors=[2, 4, 2, 4, 4, 2, 4, 2],
               plusrows=[0, 1, 1, 1, 1, 2, 3], pluscols=[2, 0, 1, 2, 3, 2, 2],
               pairwise=0),
  ]
  test = [
      generate(size=4, rows=[0, 0, 1, 1, 2, 2, 3, 3],
               cols=[0, 3, 1, 2, 1, 2, 0, 3], colors=[3, 1, 2, 2, 2, 2, 3, 3],
               plusrows=[0, 0, 1, 1, 1, 1, 2, 2, 3, 3, 3, 3],
               pluscols=[1, 2, 0, 1, 2, 3, 0, 3, 0, 1, 2, 3], pairwise=1),
  ]
  return {"train": train, "test": test}

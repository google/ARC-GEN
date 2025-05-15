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


def generate(rows=None, cols=None, idxs=None, colors=None, midrows=None,
             midcols=None, size=11, minisize=3):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices into the colors list
    colors: a list of colors for the pixels
    midrows: a list of vertical coordinates for the middle points
    midcols: a list of horizontal coordinates for the middle points
    size: the width and height of the input grid
    minisize: the width and height of the output grid
  """
  if rows is None:
    pixels = []
    for r in range(minisize):
      for c in range(minisize):
        if r == 1 and c == 1: continue
        pixels.append((r, c))
    pixels = common.shuffle(pixels)
    rows, cols = zip(*pixels)
    idxs = [0, 0, 1, 1, 2, 2, 3, 3]
    colors = [0 if color == 5 else color for color in common.random_colors(4)]
    midrows, midcols = [], []
    while len(midrows) < 4:
      midrow, midcol = common.randint(1, size - 2), common.randint(1, size - 2)
      too_close = False
      for r, c in zip(midrows, midcols):
        too_close = too_close or (abs(r - midrow) < 4 and abs(c - midcol) < 4)
      if too_close: continue
      midrows.append(midrow)
      midcols.append(midcol)

  grid, output = common.grid(size, size), common.grid(minisize, minisize)
  for r, c, color in zip(midrows, midcols, colors):
    grid[r][c] = 0 if color == 0 else common.gray()
  output[1][1] = common.gray()
  for r, c, idx in zip(rows, cols, idxs):
    grid[r + midrows[idx] - 1][c + midcols[idx] - 1] = colors[idx]
    output[r][c] = colors[idx]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 0, 1, 1, 2, 2, 2], cols=[0, 1, 2, 0, 2, 0, 1, 2],
               idxs=[0, 0, 1, 2, 1, 3, 3, 2], colors=[6, 7, 0, 4],
               midrows=[2, 8, 8, 2], midcols=[7, 5, 1, 3]),
      generate(rows=[0, 0, 0, 1, 1, 2, 2, 2], cols=[0, 1, 2, 0, 2, 0, 1, 2],
               idxs=[0, 1, 1, 2, 2, 3, 3, 3], colors=[6, 2, 7, 3],
               midrows=[3, 9, 3, 7], midcols=[2, 2, 5, 7]),
      generate(rows=[0, 0, 0, 1, 1, 2, 2, 2], cols=[0, 1, 2, 0, 2, 0, 1, 2],
               idxs=[0, 1, 1, 1, 2, 3, 3, 2], colors=[0, 1, 2, 9],
               midrows=[1, 3, 4, 8], midcols=[9, 1, 5, 7]),
  ]
  test = [
      generate(rows=[0, 0, 0, 1, 1, 2, 2, 2], cols=[0, 1, 2, 0, 2, 0, 1, 2],
               idxs=[0, 1, 2, 1, 0, 1, 3, 3], colors=[4, 9, 8, 2],
               midrows=[4, 2, 7, 9], midcols=[1, 8, 6, 3]),
  ]
  return {"train": train, "test": test}

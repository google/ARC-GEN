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


def generate(width=None, height=None, rows=None, cols=None, wides=None,
             talls=None, flips=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    rows: a list of vertical coordinates where boxes should be placed
    cols: a list of horizontal coordinates where boxes should be placed
    wides: a list of widths of the boxes
    talls: a list of heights of the boxes
    flips: a list of flips of the boxes
    colors: a list of colors of the boxes
  """
  if width is None:
    width, height = common.randint(6, 15), common.randint(6, 15)
    num_boxes = common.randint(1, 2)
    while True:  # keep trying until we get the desired number of boxes
      rows, cols, wides, talls = [], [], [], []
      for _ in range(num_boxes):
        w = common.randint(2, width - 1)
        t = common.randint(2, height - 1)
        r = common.randint(0, height - t - 1)
        c = common.randint(0, width - w - 1)
        if common.overlaps(rows + [r], cols + [c], wides + [w], talls + [t], 1):
          continue
        rows.append(r)
        cols.append(c)
        wides.append(w)
        talls.append(t)
      if len(wides) == num_boxes: break
    flips = [common.randint(0, 1) for _ in range(num_boxes)]
    colors = common.random_colors(num_boxes)

  grid, output = common.grids(width, height)
  for r, c, w, t, f, color in zip(rows, cols, wides, talls, flips, colors):
    grid[r][c + w - 1 if f else c] = color
    grid[r + t - 1][c if f else c + w - 1] = color
    for row in range(r, r + t):
      for col in range(c, c + w):
        output[row][col] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=10, height=10, rows=[1, 5], cols=[1, 3], wides=[6, 5],
               talls=[3, 3], flips=[1, 0], colors=[1, 2]),
      generate(width=8, height=7, rows=[1, 3], cols=[1, 4], wides=[2, 4],
               talls=[4, 2], flips=[0, 1], colors=[3, 7]),
      generate(width=10, height=10, rows=[2], cols=[1], wides=[5], talls=[5],
               flips=[0], colors=[4]),
      generate(width=11, height=6, rows=[1], cols=[1], wides=[7], talls=[3],
               flips=[0], colors=[7]),
  ]
  test = [
      generate(width=8, height=9, rows=[0, 4], cols=[0, 1], wides=[3, 5],
               talls=[2, 4], flips=[0, 1], colors=[8, 6]),
  ]
  return {"train": train, "test": test}

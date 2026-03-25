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


def generate(width=None, height=None, rows=None, cols=None, color=None,
             boxrows=None, boxcols=None, wides=None, talls=None, boxcolor=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    color: a digit representing a color to be used
    boxrows: a list of vertical coordinates where boxes should be placed
    boxcols: a list of horizontal coordinates where boxes should be placed
    wides: a list of widths of boxes
    talls: a list of heights of boxes
    boxcolor: a digit representing a color to be used for boxes
  """
  if width is None:
    num_boxes = common.randint(3, 5)
    colors = common.random_colors(2)
    color, boxcolor = colors[0], colors[1]
    while True:
      width, height = common.randint(10, 20), common.randint(10, 20)
      wides = [common.randint(3, 10) for _ in range(num_boxes)]
      talls = [common.randint(3, 10) for _ in range(num_boxes)]
      boxrows = [common.randint(0, height - tall) for tall in talls]
      boxcols = [common.randint(0, width - wide) for wide in wides]
      if not common.overlaps(boxrows, boxcols, wides, talls, 1): break
    pixels = common.remove_neighbors(common.random_pixels(width, height, 0.05))
    rows, cols = zip(*pixels)

  grid, output = common.grids(width, height)
  for boxrow, boxcol, wide, tall in zip(boxrows, boxcols, wides, talls):
    for r in range(boxrow, boxrow + tall):
      for c in range(boxcol, boxcol + wide):
        output[r][c] = grid[r][c] = boxcolor
  for r, c in zip(rows, cols):
    grid[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=14, height=13,
               rows=[0, 0, 0, 2, 2, 4, 5, 7, 7, 7, 8, 10, 10, 12, 12, 12],
               cols=[0, 4, 11, 8, 10, 7, 4, 1, 6, 12, 4, 4, 8, 1, 4, 13],
               color=8, boxrows=[0, 3, 6, 7, 10], boxcols=[6, 2, 9, 3, 0],
               wides=[5, 3, 5, 5, 3], talls=[5, 3, 4, 4, 3], boxcolor=3),
      generate(width=16, height=13,
               rows=[1, 2, 3, 5, 5, 8, 9, 9, 10, 10, 11, 11],
               cols=[6, 10, 3, 5, 14, 12, 1, 9, 3, 15, 9, 12], color=1,
               boxrows=[1, 2, 9], boxcols=[1, 9, 3], wides=[4, 7, 10],
               talls=[5, 5, 4], boxcolor=2),
  ]
  test = [
      generate(width=17, height=12,
               rows=[0, 1, 1, 2, 3, 5, 6, 7, 7, 9, 10, 11, 11],
               cols=[14, 1, 6, 2, 16, 7, 14, 5, 12, 15, 11, 3, 9], color=4,
               boxrows=[0, 2, 10], boxcols=[12, 1, 6], wides=[4, 8, 6],
               talls=[7, 6, 2], boxcolor=5),
  ]
  return {"train": train, "test": test}

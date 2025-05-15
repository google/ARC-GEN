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


def generate(rows=None, cols=None, minirows=None, minicols=None, colors=None,
             minisize=3, rainbow=(2, 3, 4, 6, 8)):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates identifying which mini-grid to use
    cols: a list of horizontal coordinates identifying which mini-grid to use
    minirows: a list of vertical coordinates inside the mini-grid
    minicols: a list of horizontal coordinates inside the mini-grid
    colors: a digit representing a color to be used
    minisize: the width and height of each mini-rid
    rainbow: a list of digits representing the set of "rainbow" colors
  """
  if rows is None:
    rows, cols, minirows, minicols, colors = [], [], [], [], []
    chosen_row, chosen_col = common.randint(0, 2), common.randint(0, 2)
    for r in range(minisize):
      for c in range(minisize):
        count = 4 if r == chosen_row and c == chosen_col else 5
        pixels = common.sample(common.all_pixels(minisize, minisize), count)
        rows.extend([r] * count)
        cols.extend([c] * count)
        minirows.extend([p[0] for p in pixels])
        minicols.extend([p[1] for p in pixels])
        colors.extend(rainbow[0:count])

  grid = common.hollywood_squares(minisize, common.black(), common.gray())
  output = common.hollywood_squares(minisize, common.black(), common.gray())
  m = {}
  for r, c, mr, mc, color in zip(rows, cols, minirows, minicols, colors):
    grid[r * (minisize + 1) + mr][c * (minisize + 1) + mc] = color
    m[(r, c)] = 1 if (r, c) not in m else m[(r, c)] + 1
  for r, c, mr, mc, color in zip(rows, cols, minirows, minicols, colors):
    if m[(r, c)] > 4: continue
    for dr in range(minisize):
      for dc in range(minisize):
        output[mr * (minisize + 1) + dr][mc * (minisize + 1) + dc] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1,
                     1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                     2, 2, 2, 2],
               cols=[0, 1, 1, 2, 0, 0, 1, 1, 2, 2, 0, 1, 2, 2, 0, 0, 1, 1, 2, 2,
                     0, 1, 2, 0, 0, 1, 1, 2, 2, 0, 0, 1, 2, 0, 1, 1, 2, 0, 0, 1,
                     1, 2, 2, 2],
               minirows=[0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 0, 0, 0, 0,
                         0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 1, 1, 1,
                         1, 2, 2, 2, 2, 2, 2, 2],
               minicols=[0, 1, 2, 2, 1, 2, 0, 2, 0, 2, 0, 0, 0, 2, 0, 1, 0, 1,
                         1, 2, 2, 2, 0, 0, 1, 0, 1, 1, 2, 1, 2, 1, 1, 0, 0, 2,
                         2, 0, 2, 0, 1, 0, 1, 2],
               colors=[2, 6, 2, 4, 4, 3, 4, 8, 3, 6, 6, 3, 8, 2, 3, 8, 6, 2, 4,
                       8, 4, 4, 6, 6, 2, 3, 8, 3, 2, 3, 6, 2, 6, 2, 4, 8, 8, 8,
                       4, 6, 3, 2, 3, 4]),
      generate(rows=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1,
                     1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                     2, 2, 2, 2],
               cols=[0, 0, 1, 1, 2, 0, 1, 2, 2, 0, 0, 1, 1, 2, 2, 0, 0, 1, 2, 2,
                     0, 1, 2, 0, 0, 1, 1, 2, 2, 0, 0, 1, 1, 2, 0, 0, 1, 2, 2, 0,
                     1, 1, 2, 2],
               minirows=[0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 0, 0, 0,
                         0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 1, 1,
                         1, 1, 1, 2, 2, 2, 2, 2],
               minicols=[0, 2, 0, 1, 1, 2, 2, 0, 2, 0, 1, 0, 1, 0, 2, 0, 2, 2,
                         1, 2, 2, 1, 0, 0, 2, 0, 2, 0, 2, 0, 1, 1, 2, 0, 1, 2,
                         0, 0, 2, 0, 1, 2, 0, 1],
               colors=[2, 3, 4, 6, 6, 8, 2, 4, 3, 4, 6, 3, 8, 2, 8, 4, 8, 2, 6,
                       4, 2, 3, 3, 3, 6, 4, 6, 8, 2, 3, 6, 8, 4, 2, 8, 4, 2, 8,
                       3, 2, 3, 6, 6, 4]),
      generate(rows=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1,
                     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                     2, 2, 2, 2],
               cols=[0, 1, 1, 2, 2, 0, 0, 1, 1, 2, 0, 0, 1, 2, 2, 0, 1, 1, 2, 2,
                     0, 0, 1, 1, 2, 0, 0, 1, 2, 2, 0, 0, 1, 2, 0, 1, 1, 2, 2, 0,
                     0, 1, 2, 2],
               minirows=[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 0, 0, 0,
                         0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 0, 0, 0, 0, 1, 1,
                         1, 1, 1, 2, 2, 2, 2, 2],
               minicols=[1, 1, 2, 1, 2, 0, 2, 0, 1, 2, 1, 2, 1, 0, 2, 1, 0, 2,
                         0, 1, 0, 2, 0, 2, 2, 0, 1, 1, 0, 1, 0, 1, 1, 2, 2, 1,
                         2, 0, 1, 0, 1, 0, 0, 2],
               colors=[3, 6, 3, 6, 2, 6, 4, 2, 8, 8, 2, 8, 4, 3, 4, 2, 4, 3, 3,
                       4, 4, 8, 2, 6, 2, 3, 6, 8, 8, 6, 6, 3, 3, 3, 2, 6, 4, 2,
                       8, 8, 4, 2, 4, 6]),
      generate(rows=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1,
                     1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                     2, 2, 2, 2],
               cols=[0, 0, 0, 1, 1, 2, 2, 1, 1, 2, 2, 0, 0, 1, 2, 0, 0, 1, 1, 2,
                     0, 0, 1, 2, 2, 0, 1, 1, 2, 0, 1, 1, 2, 2, 0, 0, 1, 1, 2, 0,
                     0, 1, 2, 2],
               minirows=[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 0, 0, 0,
                         0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 0, 0, 0, 0, 0, 1, 1,
                         1, 1, 1, 2, 2, 2, 2, 2],
               minicols=[0, 1, 2, 0, 1, 0, 2, 0, 2, 0, 2, 0, 1, 1, 0, 1, 2, 0,
                         2, 1, 1, 2, 2, 1, 2, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 2,
                         1, 2, 2, 0, 1, 2, 0, 2],
               colors=[3, 8, 4, 4, 6, 2, 8, 8, 3, 6, 3, 6, 2, 2, 4, 4, 2, 8, 3,
                       4, 8, 6, 4, 2, 6, 3, 2, 6, 3, 6, 6, 2, 3, 6, 3, 8, 8, 3,
                       4, 4, 2, 4, 2, 8]),
  ]
  test = [
      generate(rows=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1,
                     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                     2, 2, 2, 2],
               cols=[0, 0, 1, 2, 0, 1, 1, 1, 2, 2, 0, 0, 1, 2, 2, 0, 1, 2, 2, 2,
                     0, 0, 0, 1, 1, 1, 2, 0, 1, 2, 0, 0, 1, 1, 2, 2, 0, 0, 1, 2,
                     2, 1, 1, 2],
               minirows=[0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 0, 0, 0,
                         0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 0, 0, 0, 0, 0, 0,
                         1, 1, 1, 1, 1, 2, 2, 2],
               minicols=[0, 1, 1, 1, 2, 0, 1, 2, 0, 2, 0, 2, 0, 0, 1, 0, 1, 0,
                         1, 2, 0, 1, 2, 0, 1, 2, 2, 1, 2, 0, 1, 2, 1, 2, 1, 2,
                         1, 2, 2, 0, 2, 0, 2, 0],
               colors=[6, 4, 3, 4, 3, 2, 8, 6, 8, 2, 2, 8, 4, 6, 3, 2, 3, 3, 6,
                       2, 3, 4, 6, 8, 4, 2, 4, 8, 6, 8, 2, 4, 6, 4, 2, 8, 6, 3,
                       3, 4, 6, 2, 8, 3]),
  ]
  return {"train": train, "test": test}

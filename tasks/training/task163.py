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
             minisize=3):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates identifying which mini-grid to use
    cols: a list of horizontal coordinates identifying which mini-grid to use
    minirows: a list of vertical coordinates inside the mini-grid
    minicols: a list of horizontal coordinates inside the mini-grid
    colors: a digit representing a color to be used
    minisize: the width and height of each mini-rid
  """
  if rows is None:
    rows, cols, minirows, minicols, colors = [], [], [], [], []
    for r in range(minisize):
      for c in range(minisize):
        count = common.randint(2, 4)
        pixels = common.sample(common.all_pixels(minisize, minisize), count)
        rows.extend([r] * count)
        cols.extend([c] * count)
        minirows.extend([p[0] for p in pixels])
        minicols.extend([p[1] for p in pixels])
        colors.extend(common.random_colors(count, exclude=[common.gray(),
                                                           common.yellow()]))
    colors[common.randint(0, len(colors) - 1)] = common.yellow()

  grid = common.hollywood_squares(minisize, common.black(), common.gray())
  output = common.hollywood_squares(minisize, common.black(), common.gray())
  yellowrow, yellowcol, minirow, minicol = None, None, None, None
  for r, c, mr, mc, color in zip(rows, cols, minirows, minicols, colors):
    grid[r * (minisize + 1) + mr][c * (minisize + 1) + mc] = color
    if color != common.yellow(): continue
    yellowrow, yellowcol, minirow, minicol = r, c, mr, mc
  for r, c, mr, mc, color in zip(rows, cols, minirows, minicols, colors):
    if r != yellowrow or c != yellowcol: continue
    output[minirow * (minisize + 1) + mr][minicol * (minisize + 1) + mc] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1,
                     1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
               cols=[0, 1, 1, 2, 2, 0, 1, 2, 0, 0, 1, 2, 0, 0, 1, 1, 2, 2, 0, 1,
                     2, 0, 1, 2, 0, 0, 1, 2, 2, 0, 1, 1, 2, 0, 1, 2],
               minirows=[0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0,
                         1, 1, 1, 2, 2, 2, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2],
               minicols=[0, 0, 2, 0, 2, 2, 1, 1, 0, 1, 2, 1, 0, 2, 0, 1, 1, 2,
                         2, 2, 2, 0, 0, 1, 1, 2, 1, 0, 2, 0, 0, 2, 2, 2, 1, 1],
               colors=[3, 7, 6, 8, 7, 9, 3, 6, 7, 2, 2, 3, 7, 2, 8, 7, 2, 3, 6,
                       3, 7, 3, 2, 6, 3, 4, 2, 2, 7, 7, 7, 3, 1, 2, 6, 3]),
      generate(rows=[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2,
                     2],
               cols=[0, 1, 2, 0, 2, 0, 1, 0, 0, 0, 1, 2, 2, 0, 1, 2, 0, 1, 2,
                     1],
               minirows=[0, 0, 0, 1, 1, 2, 2, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1,
                         1, 2],
               minicols=[0, 1, 1, 2, 2, 1, 1, 1, 0, 2, 2, 1, 2, 0, 1, 1, 1, 2,
                         2, 0],
               colors=[3, 2, 6, 7, 9, 6, 1, 3, 1, 9, 6, 7, 3, 9, 9, 9, 6, 4, 1,
                       7]),
      generate(rows=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2,
                     2, 2, 2, 2, 2, 2, 2],
               cols=[0, 1, 2, 0, 0, 0, 2, 1, 0, 0, 1, 2, 1, 2, 2, 0, 2, 0, 1, 0,
                     1, 2, 2, 0, 1, 2, 2],
               minirows=[0, 0, 0, 1, 1, 1, 1, 2, 0, 0, 0, 0, 1, 1, 1, 2, 2, 0,
                         0, 1, 1, 1, 1, 2, 2, 2, 2],
               minicols=[1, 1, 0, 0, 1, 2, 1, 1, 1, 2, 1, 2, 0, 1, 2, 2, 0, 1,
                         1, 0, 0, 0, 2, 1, 1, 1, 2],
               colors=[7, 6, 7, 8, 3, 6, 8, 3, 8, 7, 3, 7, 8, 8, 6, 6, 3, 6, 8,
                       8, 3, 4, 8, 7, 6, 6, 7]),
      generate(rows=[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2,
                     2, 2],
               cols=[0, 1, 2, 0, 1, 2, 0, 2, 0, 0, 1, 1, 2, 2, 0, 1, 2, 1, 2, 0,
                     1, 2],
               minirows=[0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 2, 0, 0, 0, 1,
                         1, 2, 2, 2],
               minicols=[0, 1, 2, 1, 1, 1, 1, 1, 0, 2, 0, 2, 1, 1, 0, 1, 2, 1,
                         0, 1, 1, 2],
               colors=[3, 1, 2, 2, 3, 6, 1, 3, 7, 6, 2, 7, 7, 6, 7, 4, 3, 7, 2,
                       3, 3, 6]),
  ]
  test = [
      generate(rows=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1,
                     1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
               cols=[0, 0, 1, 2, 0, 0, 1, 2, 2, 1, 1, 2, 0, 2, 2, 0, 1, 1, 2, 0,
                     0, 1, 2, 0, 1, 2, 2, 0, 1, 0, 1, 2, 2],
               minirows=[0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 0, 0, 0, 1, 1, 1,
                         1, 2, 2, 2, 2, 0, 0, 0, 0, 1, 1, 2, 2, 2, 2],
               minicols=[0, 2, 0, 1, 0, 1, 1, 0, 1, 0, 2, 2, 0, 0, 2, 1, 1, 2,
                         1, 0, 2, 1, 1, 0, 1, 0, 1, 2, 1, 0, 1, 1, 2],
               colors=[2, 3, 2, 3, 7, 6, 7, 6, 7, 6, 3, 2, 7, 6, 4, 6, 2, 7, 2,
                       6, 2, 3, 7, 7, 6, 2, 3, 6, 2, 2, 7, 6, 7]),
  ]
  return {"train": train, "test": test}

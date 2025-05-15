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
             colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where punchcards should be placed
    cols: a list of horizontal coordinates where punchcards should be placed
    wides: a list of punchcard widths
    colors: a list of colors to be used for the punchcards
  """
  if rows is None:
    width, height = 10 * common.randint(2, 3), common.randint(8, 16)
    r, rows, cols, wides = 1, [], [], []
    while r + 2 < height:
      rows.append(r)
      wides.append(2 * common.randint(2, width // 2) - 1)
      cols.append(common.randint(0, width - wides[-1]))
      r += common.randint(3, 4)
    colors = common.random_colors(len(wides))

  grid, output = common.grids(width, height)
  for row, col, wide, color in zip(rows, cols, wides, colors):
    for r in range(3):
      for c in range(wide):
        grid[row + r][col + c] = color
        if r != 1 or c % 2 == 0: output[row + r][col + c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=30, height=8, rows=[1, 5], cols=[0, 12], wides=[29, 13],
               colors=[4, 8]),
      generate(width=20, height=8, rows=[1, 5], cols=[1, 7], wides=[9, 11],
               colors=[1, 7]),
  ]
  test = [
      generate(width=20, height=11, rows=[1, 5, 8], cols=[2, 1, 15],
               wides=[7, 13, 5], colors=[5, 4, 8]),
  ]
  return {"train": train, "test": test}

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


def generate(rows=None, cols=None, wides=None, talls=None, colors=None, size=8):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates for the cutouts
    cols: a list of horizontal coordinate for the cutouts
    wides: a list of widths of the cutouts
    talls: a list of heights of the cutouts
    colors: a list of colors to be used
    size: the width and height of one quarter of the grid
  """
  if rows is None:
    # TODO: Make sure we don't cut out the center.
    wides = [common.randint(2, 4) for _ in range(2)]
    talls = [common.randint(2, 4) for _ in range(2)]
    rows = [common.randint(0, size - tall) for tall in talls]
    cols = [common.randint(0, size - wide) for wide in wides]
    bitmap = common.grid(size, size, common.yellow())
    for j in range(size):
      for i in range(j + 1):
        color = common.random_color(exclude=[common.yellow()])
        bitmap[i][j] = bitmap[j][i] = color
    colors = []
    for r in bitmap:
      colors.extend(r)

  grid, output = common.grids(2 * size, 2 * size, common.yellow())
  for r in range(size):
    for c in range(size):
      color = colors[r * size + c]
      for bitmap in [grid, output]:
        bitmap[r][c] = bitmap[2 * size - r - 1][2 * size - c - 1] = color
        bitmap[r][2 * size - c - 1] = bitmap[2 * size - r - 1][c] = color
  for row, col, wide, tall in zip(rows, cols, wides, talls):
    for r in range(tall):
      for c in range(wide):
        grid[row + r][col + c] = common.yellow()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[5, 10], cols=[10, 10], wides=[4, 3], talls=[3, 4],
               colors=[9, 9, 6, 5, 9, 6, 7, 7, 9, 1, 5, 5, 6, 1, 7, 9, 6, 5, 1,
                       9, 7, 7, 3, 3, 5, 5, 9, 3, 7, 9, 3, 3, 9, 6, 7, 7, 3, 8,
                       9, 1, 6, 1, 7, 9, 8, 3, 1, 1, 7, 7, 3, 3, 9, 1, 6, 6, 7,
                       9, 3, 3, 1, 1, 6, 1]),
      generate(rows=[2, 8], cols=[1, 11], wides=[2, 3], talls=[3, 2],
               colors=[9, 9, 6, 1, 8, 9, 6, 6, 9, 6, 1, 3, 9, 6, 6, 1, 6, 1, 5,
                       2, 6, 6, 8, 8, 1, 3, 2, 8, 6, 1, 8, 2, 8, 9, 6, 6, 7, 1,
                       5, 5, 9, 6, 6, 1, 1, 1, 5, 5, 6, 6, 8, 8, 5, 5, 9, 5, 6,
                       1, 8, 2, 5, 5, 5, 8]),
      generate(rows=[6, 11], cols=[12, 2], wides=[2, 4], talls=[4, 4],
               colors=[9, 3, 9, 9, 2, 8, 7, 8, 3, 9, 9, 3, 8, 8, 8, 5, 9, 9, 2,
                       8, 7, 8, 2, 2, 9, 3, 8, 8, 8, 5, 2, 1, 2, 8, 7, 8, 2, 5,
                       9, 7, 8, 8, 8, 5, 5, 5, 7, 6, 7, 8, 2, 2, 9, 7, 1, 1, 8,
                       5, 2, 1, 7, 6, 1, 3]),
      generate(rows=[1, 8], cols=[10, 3], wides=[4, 2], talls=[3, 3],
               colors=[2, 2, 7, 6, 8, 9, 9, 1, 2, 1, 6, 2, 9, 5, 1, 1, 7, 6, 3,
                       3, 9, 1, 6, 6, 6, 2, 3, 8, 1, 1, 6, 6, 8, 9, 9, 1, 1, 7,
                       1, 1, 9, 5, 1, 1, 7, 7, 1, 3, 9, 1, 6, 6, 1, 1, 3, 3, 1,
                       1, 6, 6, 1, 3, 3, 2]),
  ]
  test = [
      generate(rows=[2, 4], cols=[6, 10], wides=[3, 4], talls=[3, 4],
               colors=[7, 7, 8, 1, 9, 8, 2, 6, 7, 1, 1, 8, 8, 8, 6, 6, 8, 1, 6,
                       9, 2, 6, 6, 1, 1, 8, 9, 1, 6, 6, 1, 1, 9, 8, 2, 6, 8, 7,
                       6, 6, 8, 8, 6, 6, 7, 7, 6, 5, 2, 6, 6, 1, 6, 6, 5, 5, 6,
                       6, 1, 1, 6, 5, 5, 7]),
  ]
  return {"train": train, "test": test}

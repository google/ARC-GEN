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


def generate(
    width=None,
    height=None,
    rows=None,
    cols=None,
    wides=None,
    talls=None,
    colors=None,
    tongue=None,
    flip=None,
    xpose=None,
):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    wides: a list of box widths
    talls: a list of box heights
    colors: a list of digits representing the colors to be used
    tongue: the placement of the frog's tongue
    flip: a boolean indicating whether the grids should be flipped
    xpose: a boolean indicating whether the grids should be transposed  
  """
  if width is None:
    # Choose the frog & fly body sizes
    width, height = common.randint(12, 20), common.randint(15, 20)
    wides = [common.randint(7, 8), common.randint(3, 5)]
    talls = [common.randint(3, 8), common.randint(3, 4)]
    # Make the fly smaller than the frog, and choose their respective columns.
    talls[1] = min(talls[0], talls[1])
    cols = [common.randint(1, width - wides[0] - 1)]
    cols += [cols[0] + common.randint(0, wides[0] - wides[1])]
    tongue = common.randint(cols[1], cols[1] + wides[1] - 1)
    # Sometimes we make the *fly* bigger!
    if common.randint(0, 1):
      wides, talls, cols = wides[::-1], talls[::-1], cols[::-1]
    # Choose the rows (which requires extrapolating the tongue length)
    tongue_length = common.randint(1, height - talls[0] - talls[1] - 2)
    body_length = talls[0] + talls[1] + tongue_length
    rows = [common.randint(1, height - body_length - 1)]
    rows += [rows[0] + talls[0] + tongue_length]
    # Finally, pick the colors, and whether we flip and/or transpose the grids.
    colors = common.random_colors(2)
    flip, xpose = common.randint(0, 1), common.randint(0, 1)

  grid, output = common.grids(width, height)
  for i, color in enumerate(colors):
    row, col, wide, tall = rows[i], cols[i], wides[i], talls[i]
    for r in range(tall):
      for c in range(wide):
        grid[row + r][col + c] = color
        output[(row if not i else (rows[0] + talls[0])) + r][col + c] = color
  for r in range(rows[0] + talls[0], rows[1]):
    grid[r][tongue] = colors[1]
  if flip: grid, output = grid[::-1], output[::-1]
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=14, height=17, rows=[1, 8], cols=[1, 2], wides=[7, 4],
               talls=[3, 3], colors=[4, 5], tongue=3, flip=0, xpose=0),
      generate(width=13, height=18, rows=[4, 14], cols=[3, 5], wides=[7, 3],
               talls=[7, 3], colors=[2, 4], tongue=6, flip=1, xpose=1),
      generate(width=19, height=15, rows=[1, 7], cols=[6, 3], wides=[5, 8],
               talls=[2, 6], colors=[2, 3], tongue=7, flip=0, xpose=0),
  ]
  test = [
      generate(width=12, height=17, rows=[1, 11], cols=[3, 4], wides=[8, 3],
               talls=[5, 4], colors=[3, 7], tongue=4, flip=0, xpose=1),
  ]
  return {"train": train, "test": test}

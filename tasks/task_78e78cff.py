# Copyright 2026 Google LLC
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


def generate(width=None, height=None, wide=None, tall=None, brow=None,
             bcol=None, prow=None, pcol=None, colors=None, erows=None,
             ecols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grids.
    height: The height of the grids.
    wide: The width of the inner rectangle.
    tall: The height of the inner rectangle.
    brow: The row of the rectangle.
    bcol: The column of the rectangle.
    prow: The row of the inner pixel.
    pcol: The column of the inner pixel.
    colors: The colors to use.
    erows: The rows of the empty cells.
    ecols: The columns of the empty cells.
  """

  def draw():
    # Check that the corners are mostly there.
    if not erows or not ecols: return None, None
    epixels = list(zip(erows, ecols))
    w, t = wide - 1, tall - 1
    if (0, 0) in epixels:
      if (0, 1) in epixels or (1, 0) in epixels: return None, None
    if (0, w) in epixels:
      if (0, w - 1) in epixels or (1, w) in epixels: return None, None
    if (t, 0) in epixels:
      if (t - 1, 0) in epixels or (t, 1) in epixels: return None, None
    if (t, w) in epixels:
      if (t - 1, w) in epixels or (t, w - 1) in epixels: return None, None
    # Now draw the grids.
    grid, output = common.grids(width, height, colors[0])
    common.hollow_rect(grid, wide, tall, brow, bcol, colors[1])
    common.hollow_rect(output, wide, tall, brow, bcol, colors[1])
    common.rect(output, wide - 2, tall - 2, brow + 1, bcol + 1, colors[2])
    grid[prow][pcol] = colors[2]
    for erow, ecol in zip(erows, ecols):
      grid[brow + erow][bcol + ecol] = colors[0]
      output[brow + erow][bcol + ecol] = colors[0]
      if erow not in [0, tall - 1]:
        start = 0 if ecol == 0 else ecol + 1
        end = bcol + 1 if ecol == 0 else width
        for col in range(start, end):
          output[brow + erow][col] = colors[2]
      if ecol not in [0, wide - 1]:
        start = 0 if erow == 0 else erow + 1
        end = brow + 1 if erow == 0 else height
        for row in range(start, end):
          output[row][bcol + ecol] = colors[2]
    return grid, output

  if width is None:
    width, height = common.randint(11, 12), common.randint(11, 12)
    wide, tall = common.randint(5, width - 4), common.randint(5, height - 4)
    brow = common.randint(2, height - tall - 2)
    bcol = common.randint(2, width - wide - 2)
    prow = common.randint(brow + 1, brow + tall - 2)
    pcol = common.randint(bcol + 1, bcol + wide - 2)
    colors = common.random_colors(3)
    symmetry = common.randint(0, 1)
    while True:
      erows, ecols = [], []
      for row in range(tall):
        for col in range(wide):
          if row not in [0, tall - 1] and col not in [0, wide - 1]: continue
          if common.randint(0, 2): continue
          erows.append(row)
          ecols.append(col)
          erows.append(row if symmetry else tall - 1 - row)
          ecols.append(wide - 1 - col if symmetry else col)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=11, height=11, wide=5, tall=6, brow=2, bcol=2, prow=5,
               pcol=4, colors=[3, 1, 6], erows=[0, 1, 2, 2, 3, 3, 4, 5],
               ecols=[2, 4, 0, 4, 0, 4, 4, 2]),
      generate(width=12, height=11, wide=8, tall=5, brow=2, bcol=2, prow=5,
               pcol=5, colors=[1, 2, 3],
               erows=[0, 0, 0, 0, 0, 0, 2, 2, 4, 4, 4, 4, 4, 4],
               ecols=[0, 2, 3, 4, 5, 7, 0, 7, 0, 2, 3, 4, 5, 7]),
  ]
  test = [
      generate(width=12, height=12, wide=7, tall=7, brow=2, bcol=2, prow=6,
               pcol=6, colors=[4, 2, 8], erows=[0, 0, 0, 0, 0, 3, 3, 6, 6, 6],
               ecols=[0, 2, 3, 4, 6, 0, 6, 0, 3, 6])
  ]
  return {"train": train, "test": test}

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


def generate(width=None, height=None, row=None, cols=None, colors=None,
             brow=None, bcol=None, prows=None, pcols=None, flop=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    rows: The rows of the boxes.
    cols: The columns of the boxes.
    thicks: The thicknesses of the boxes.
  """

  def draw():
    grid, output = common.grids(width, height)
    for i, (col, color) in enumerate(zip(cols, colors)):
      output[row][col] = grid[row][col] = color
      for prow, pcol in zip(prows, pcols):
        r, c = brow + prow, bcol + 2 * i + col + pcol - cols[0]
        if r >= height or c >= width: return None, None
        if not i: grid[r][c] = color
        output[r][c] = color
    if flop: grid, output = common.flop(grid), common.flop(output)
    if xpose: grid, output = common.transpose(grid), common.transpose(output)
    return grid, output

  if width is None:
    while True:
      width = common.randint(21, 24)
      height = common.randint(12, 18)
      row = common.randint(1, 2)
      brow, bcol = common.randint(6, 10), common.randint(1, 2)
      colors, cols = [2], [common.randint(1, 2)]
      extra = common.randint(2, 4)
      colors.extend(common.choices([3, 4, 8], extra))
      for _ in range(extra):
        cols.append(cols[-1] + common.randint(2, 5))
      prows, pcols = common.conway_sprite(3, 3, 3)
      if not common.connected(list(zip(prows, pcols))): continue
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=23, height=17, row=1, cols=[1, 3, 6, 11],
               colors=[2, 4, 4, 3], brow=9, bcol=2, prows=[0, 0, 1, 1, 2, 2],
               pcols=[0, 2, 1, 2, 0, 2], flop=False, xpose=True),
      generate(width=22, height=16, row=1, cols=[2, 5, 8, 12],
               colors=[2, 8, 3, 8], brow=8, bcol=1, prows=[0, 0, 0, 1, 2, 2, 2],
               pcols=[0, 1, 2, 1, 0, 1, 2], flop=False, xpose=False),
      generate(width=23, height=14, row=2, cols=[1, 4, 7, 12],
               colors=[2, 3, 3, 8], brow=7, bcol=2, prows=[0, 0, 0, 1, 1, 2, 2],
               pcols=[0, 1, 2, 0, 2, 1, 2], flop=True, xpose=True),
  ]
  test = [
      generate(width=24, height=13, row=1, cols=[2, 4, 7, 11, 14],
               colors=[2, 8, 8, 4, 3], brow=6, bcol=1, prows=[0, 1, 1, 1, 2, 2],
               pcols=[1, 0, 1, 2, 1, 2], flop=True, xpose=False),
  ]
  return {"train": train, "test": test}

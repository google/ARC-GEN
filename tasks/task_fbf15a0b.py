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


def generate(width=None, height=None, fgcolor=None, wides=None, talls=None,
             brows=None, bcols=None, flip=None, flop=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    fgcolor: The foreground color.
    wides: The widths of the boxes.
    talls: The heights of the boxes.
    brows: The row indices of the boxes.
    bcols: The column indices of the boxes.
    flip: Whether to flip the grid.
    flop: Whether to flop the grid.
    xpose: Whether to transpose the grid.
  """

  def draw():
    if common.overlaps(brows, bcols, wides, talls): return None, None
    grid = common.grid(width, height, 8)
    output = common.grid(width, height // 2, 8)
    for wide, tall, brow, bcol in zip(wides, talls, brows, bcols):
      for row in range(tall):
        for col in range(wide):
          if row % 2 != 0 or col % 2 != 0: continue
          grid[brow + row][bcol + col] = fgcolor
          if brow + row < height // 2: output[brow + row][bcol + col] = fgcolor
    grid[0][0] = grid[2][0] = 5
    output[0][0] = output[2][0] = 8
    if flip: grid, output = common.flip(grid), common.flip(output)
    if flop: grid, output = common.flop(grid), common.flop(output)
    if xpose: grid, output = common.transpose(grid), common.transpose(output)
    if len(set(common.flatten(output))) != 2: return None, None
    return grid, output

  if width is None:
    width, height = 2 * common.randint(2, 15), 2 * common.randint(4, 15)
    fgcolor = common.random_color(exclude=[8])
    flip = common.randint(0, 1)
    flop = common.randint(0, 1)
    xpose = common.randint(0, 1)
    while True:
      num_boxes = common.randint(1, 4)
      wides = [2 * common.randint(2, width // 2) - 1 for _ in range(num_boxes)]
      talls = [2 * common.randint(2, height // 2) - 1 for _ in range(num_boxes)]
      brows = [common.randint(0, height - tall) for tall in talls]
      bcols = [common.randint(0, width - wide) for wide in wides]
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=20, height=20, fgcolor=1, wides=[19, 19, 19],
               talls=[5, 3, 5], brows=[2, 7, 10], bcols=[1, 1, 1], flip=0,
               flop=0, xpose=0),
      generate(width=10, height=20, fgcolor=7, wides=[7, 7, 7], talls=[3, 5, 3],
               brows=[1, 6, 13], bcols=[2, 2, 2], flip=0, flop=1, xpose=0),
      generate(width=30, height=16, fgcolor=3, wides=[5, 5, 3, 5],
               talls=[11, 9, 9, 9], brows=[3, 4, 4, 4], bcols=[2, 10, 18, 24],
               flip=1, flop=0, xpose=0),
      generate(width=10, height=22, fgcolor=4, wides=[5, 5], talls=[5, 5],
               brows=[2, 13], bcols=[2, 3], flip=0, flop=0, xpose=1),
  ]
  test = [
      generate(width=4, height=8, fgcolor=9, wides=[3], talls=[7], brows=[0],
               bcols=[0], flip=1, flop=0, xpose=1),
      generate(width=10, height=28, fgcolor=2, wides=[7], talls=[23], brows=[2],
               bcols=[1], flip=1, flop=1, xpose=1),
  ]
  return {"train": train, "test": test}

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


def generate(rows=None, cols=None, wide=None, tall=None, brow=None, bcol=None,
             xpose=None, size=15):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    wide: the width of the box
    tall: the height of the box
    brow: the vertical coordinate of the top of the box
    bcol: the horizontal coordinate of the left of the box
    xpose: whether to transpose the grids
    size: the width and height of the (square) grid
  """
  if rows is None:
    wide, tall = common.randint(5, 7), common.randint(8, 9)
    brow, bcol = 3, common.randint(2, 5)
    while True:
      pixels = common.random_pixels(wide - 2, tall - 4, 0.75)
      rows, cols = zip(*pixels)
      if tall % 2:  # If height is odd, we can't have pixels in the middle.
        rows = [r if r * 2 != tall - 5 else 0 for r in rows]
      # Make sure the two halves are diagonnally connected.
      top = [(r, c) for r, c in zip(rows, cols) if r * 2 < tall - 5]
      bottom = [(r, c) for r, c in zip(rows, cols) if r * 2 > tall - 5]
      if not common.diagonally_connected(top): continue
      if not common.diagonally_connected(bottom): continue
      # Make sure the two halves are centrally aligned.
      top_mid = (min(c for _, c in top) + max(c for _, c in top) + 1) / 2
      bot_mid = (min(c for _, c in bottom) + max(c for _, c in bottom) + 1) / 2
      if top_mid != bot_mid: continue
      break
    xpose = common.randint(0, 1)

  grid, output = common.grids(size, size)
  # First, draw the red grippers.
  for c in range(bcol, bcol + wide):
    output[brow][c] = grid[brow][c] = common.red()
    output[brow + tall - 1][c] = grid[brow + tall - 1][c] = common.red()
  for bitmap in [grid, output]:
    bitmap[brow + 1][bcol] = common.red()
    bitmap[brow + 1][bcol + wide - 1] = common.red()
    bitmap[brow + tall - 2][bcol] = common.red()
    bitmap[brow + tall - 2][bcol + wide - 1] = common.red()
  # Then, draw the contents inside / outside the box.
  for r, c in zip(rows, cols):
    if r < (tall - 1) // 2 - 1:
      grid[brow - r - 2][bcol + c + 1] = common.gray()
    else:
      grid[brow - r + 1 + tall + (tall - 1) // 2][bcol + c + 1] = common.gray()
    output[brow + r + 2][bcol + c + 1] = common.gray()
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": output, "output": grid}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 0, 1, 1, 3], cols=[1, 2, 3, 1, 3, 2], wide=7, tall=8,
               brow=4, bcol=4, xpose=0),
      generate(rows=[0, 0, 1, 1, 3, 3, 3, 3], cols=[1, 4, 2, 3, 1, 2, 3, 4],
               wide=8, tall=8, brow=3, bcol=3, xpose=1),
      generate(rows=[0, 0, 1, 1, 3, 3, 3], cols=[0, 1, 1, 2, 0, 1, 2],
               wide=5, tall=8, brow=3, bcol=3, xpose=1),
  ]
  test = [
      generate(rows=[0, 0, 0, 0, 1, 1, 1, 3, 3, 3],
               cols=[1, 2, 3, 4, 0, 1, 2, 1, 2, 3],
               wide=7, tall=8, brow=4, bcol=4, xpose=0),
  ]
  return {"train": train, "test": test}

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


def generate(width=None, height=None, color=None, brow=None, bcol=None,
             prow=None, pcol=None, turns=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grids.
    height: The height of the grids.
    color: The color to use for the pixel.
    brow: The row of the box.
    bcol: The column of the box.
    prow: The row of the pixel.
    pcol: The column of the pixel.
    turns: The turns to make for the spiral.
  """

  def draw():
    if abs(turns[-1]) == 2: return None, None  # Don't end on a tiny segment.
    for i in range(len(turns) - 1):  # Check that we don't turn in on itself
      if abs(turns[i]) == 2 and (turns[i] < 0) == (turns[i + 1] < 0):
        return None, None
    grid, output = common.grid(width, height), common.grid(width, height, color)
    common.hollow_rect(grid, 3, 3, brow - 1, bcol - 1, 4)
    grid[brow][bcol] = color
    r, c, rdir, cdir = prow, pcol, -1, 0
    for turn in turns:
      mult = 1 if turn > 0 else -1
      rdir, cdir = (0, -mult * rdir) if rdir else (mult * cdir, 0)
      for _ in range(abs(turn) - 1):
        if r < 1 or r > height - 2 or c < 1 or c > width - 2:
          return None, None
        grid[r][c], r, c = 5, r + rdir, c + cdir
      if r < 1 or r > height - 2 or c < 1 or c > width - 2:
        return None, None
      grid[prow][pcol], grid[r][c] = color, 4
    row, col = brow + r - prow, bcol + c - pcol
    if row < 2 or row > height - 3 or col < 2 or col > width - 3:
      return None, None
    common.hollow_rect(output, 3, 3, row - 1, col - 1, 4)
    for i in range(2, 30):
      common.draw(output, row - i, col - i, 4)
      common.draw(output, row - i, col + i, 4)
      common.draw(output, row + i, col - i, 4)
      common.draw(output, row + i, col + i, 4)
    # Make sure the area around the box is empty.
    for row in range(brow - 2, brow + 3):
      for col in range(bcol - 2, bcol + 3):
        if brow - 2 < row < brow + 2 and bcol - 2 < col < bcol + 2: continue
        if grid[row][col]: return None, None
    return grid, output

  if width is None:
    width, height = common.randint(10, 30), common.randint(10, 30)
    color = common.random_color(exclude=[4, 5])
    while True:
      brow, bcol = common.randint(2, height - 3), common.randint(2, width - 3)
      prow, pcol = common.randint(1, height - 2), common.randint(1, width - 2)
      turns = []
      if common.randint(0, 1): turns.append(1 if common.randint(0, 1) else -1)
      for _ in range(common.randint(1, 3)):
        turn = common.randint(2, 6)
        if common.randint(0, 1): turn *= -1
        turns.append(turn)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=20, height=15, color=7, brow=8, bcol=5, prow=1, pcol=14,
               turns=[4, 4, 3]),
      generate(width=30, height=30, color=3, brow=13, bcol=16, prow=25, pcol=7,
               turns=[4, 4]),
      generate(width=30, height=30, color=8, brow=12, bcol=11, prow=19, pcol=24,
               turns=[1, 6]),
  ]
  test = [
      generate(width=13, height=12, color=1, brow=2, bcol=6, prow=2, pcol=2,
               turns=[1, 6, -5]),
      generate(width=20, height=25, color=6, brow=10, bcol=7, prow=21, pcol=17,
               turns=[-2, 3, -3]),
  ]
  return {"train": train, "test": test}

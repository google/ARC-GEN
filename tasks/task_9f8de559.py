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


def generate(colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
  """

  if colors is None:
    while True:  # Try to avoid a really thick border
      wide, tall = common.randint(9, 12), common.randint(9, 12)
      brow, bcol = common.randint(1, 13 - tall), common.randint(1, 13 - wide)
      if brow >= 4 or bcol >= 4: continue
      if brow + tall <= 10 or bcol + wide <= 10: continue
      break
    grid = common.grid(14, 14)
    common.rect(grid, wide, tall, brow, bcol, 7)
    # Draw a bunch of rectangles until they completely cover the border.
    while True:
      val = common.randint(1, 14)
      pos = common.randint(0, 14 - val)
      angle = common.randint(0, 3)
      color = common.choice([5, 8, 9])
      if angle == 0:
        if pos < bcol or pos + val > bcol + wide: pos, val = 0, 14
        common.rect(grid, val, brow, 0, pos, color)
      elif angle == 1:
        if pos < bcol or pos + val > bcol + wide: pos, val = 0, 14
        common.rect(grid, val, 14 - (brow + tall), brow + tall, pos, color)
      elif angle == 2:
        if pos < brow or pos + val > brow + tall: pos, val = 0, 14
        common.rect(grid, bcol, val, pos, 0, color)
      elif angle == 3:
        if pos < brow or pos + val > brow + tall: pos, val = 0, 14
        common.rect(grid, 14 - (bcol + wide), val, pos, bcol + wide, color)
      colors = common.flatten(grid)
      if 0 not in colors and len(set(colors)) == 4: break
    # Draw a pink line with a red tip
    cdir, line = common.randint(0, 3), []
    if cdir == 0:
      row, col = common.randint(1, tall - 2), common.randint(1, wide - 6)
      line = [(brow + row, bcol + col + i) for i in range(5)]
    if cdir == 1:
      row, col = common.randint(1, tall - 6), common.randint(1, wide - 2)
      line = [(brow + row + i, bcol + col) for i in range(5)]
    if cdir == 2:
      row, col = common.randint(1, tall - 6), common.randint(1, wide - 6)
      line = [(brow + row + i, bcol + col + i) for i in range(5)]
    if cdir == 3:
      row, col = common.randint(1, tall - 6), common.randint(1, wide - 6)
      line = [(brow + row + i, bcol + col + 4 - i) for i in range(5)]
    for row, col in line:
      grid[row][col] = 6
    point = common.randint(-1, 0)
    grid[line[point][0]][line[point][1]] = 2
    colors = common.flatten(grid)

  grid, output = common.grids(14, 14)
  prow, pcol = 0, 0
  for i, color in enumerate(colors):
    output[i // 14][i % 14] = grid[i // 14][i % 14] = color
    if color == 2: prow, pcol = i // 14, i % 14
  rdir, cdir = 0, 0
  if 6 in [grid[prow - 1][pcol - 1],
           grid[prow - 1][pcol],
           grid[prow - 1][pcol + 1]]: rdir = 1
  if 6 in [grid[prow + 1][pcol - 1],
           grid[prow + 1][pcol],
           grid[prow + 1][pcol + 1]]: rdir = -1
  if 6 in [grid[prow - 1][pcol - 1],
           grid[prow][pcol - 1],
           grid[prow + 1][pcol - 1]]: cdir = 1
  if 6 in [grid[prow - 1][pcol + 1],
           grid[prow][pcol + 1],
           grid[prow + 1][pcol + 1]]: cdir = -1
  while grid[prow][pcol] in [2, 7]: prow, pcol = prow + rdir, pcol + cdir
  output[prow][pcol] = 7
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 5, 5,
                       5, 5, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 5,
                       5, 5, 7, 7, 7, 7, 7, 7, 7, 6, 7, 7, 5, 5,
                       9, 9, 7, 7, 7, 7, 7, 7, 7, 6, 7, 7, 5, 5,
                       9, 9, 7, 7, 7, 7, 7, 7, 7, 6, 7, 7, 5, 5,
                       5, 5, 7, 7, 7, 7, 7, 7, 7, 6, 7, 7, 5, 5,
                       5, 5, 7, 7, 7, 7, 7, 7, 7, 2, 7, 7, 5, 5,
                       5, 5, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 5,
                       5, 5, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 5,
                       5, 5, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 5,
                       5, 5, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 5,
                       5, 5, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 5,
                       5, 5, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 5,
                       5, 5, 8, 5, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8]),
      generate(colors=[5, 5, 5, 5, 5, 5, 5, 5, 9, 9, 5, 5, 5, 5,
                       5, 5, 5, 5, 5, 5, 5, 5, 9, 9, 5, 5, 5, 5,
                       8, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9, 9, 9,
                       8, 8, 7, 7, 7, 2, 7, 7, 7, 7, 7, 9, 9, 9,
                       8, 8, 7, 7, 7, 7, 6, 7, 7, 7, 7, 9, 9, 9,
                       8, 8, 7, 7, 7, 7, 7, 6, 7, 7, 7, 9, 9, 9,
                       8, 8, 7, 7, 7, 7, 7, 7, 6, 7, 7, 9, 9, 9,
                       8, 8, 7, 7, 7, 7, 7, 7, 7, 6, 7, 9, 9, 9,
                       8, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9, 9, 9,
                       8, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9, 9, 9,
                       8, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9, 9, 9,
                       8, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8,
                       8, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8,
                       5, 5, 9, 9, 5, 5, 5, 5, 5, 5, 5, 8, 8, 8]),
      generate(colors=[9, 9, 9, 9, 9, 9, 5, 5, 9, 9, 9, 9, 9, 9,
                       9, 9, 9, 9, 9, 9, 5, 5, 9, 9, 9, 9, 9, 9,
                       9, 9, 9, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 5,
                       9, 9, 9, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 5,
                       9, 9, 9, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 5,
                       9, 9, 9, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 5,
                       9, 9, 9, 7, 7, 7, 2, 6, 6, 6, 6, 7, 5, 5,
                       9, 9, 9, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 5,
                       9, 9, 9, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 5,
                       9, 9, 9, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 5,
                       9, 9, 9, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 5,
                       9, 9, 9, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 5,
                       9, 9, 9, 8, 8, 8, 8, 8, 9, 8, 8, 8, 8, 8,
                       9, 9, 9, 8, 8, 8, 8, 8, 9, 8, 8, 8, 8, 8]),
      generate(colors=[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       9, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8,
                       9, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8,
                       9, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8,
                       9, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8,
                       9, 7, 7, 6, 6, 6, 6, 2, 7, 7, 7, 8, 8, 8,
                       9, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8,
                       9, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8,
                       9, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9, 9, 9,
                       9, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8,
                       9, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8,
                       9, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8,
                       5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 8, 8, 8,
                       5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 8, 8, 8]),
  ]
  test = [
      generate(colors=[8, 8, 9, 9, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 9, 9, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 9, 9, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9,
                       8, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 6, 7, 9,
                       8, 8, 7, 7, 7, 7, 7, 7, 7, 7, 6, 7, 7, 9,
                       8, 8, 7, 7, 7, 7, 7, 7, 7, 6, 7, 7, 7, 9,
                       8, 8, 7, 7, 7, 7, 7, 7, 6, 7, 7, 7, 7, 9,
                       8, 8, 7, 7, 7, 7, 7, 2, 7, 7, 7, 7, 7, 9,
                       8, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9,
                       8, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9,
                       8, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9,
                       5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 9, 5, 5, 9,
                       5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 9, 5, 5, 9]),
  ]
  return {"train": train, "test": test}

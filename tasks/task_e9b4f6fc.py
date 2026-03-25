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


def generate(wide=None, tall=None, brow=None, bcol=None, prows=None, pcols=None,
             lefts=None, rites=None, pattern=None):
  """Returns input and output grids according to the given parameters.

  Args:
    wide: The width of the output grid.
    tall: The height of the output grid.
    brow: The row of the first pattern color.
    bcol: The column of the first pattern color.
    prows: The rows of the pair colors.
    pcols: The columns of the pair colors.
    lefts: The left colors of the pair colors.
    rites: The right colors of the pair colors.
    pattern: The pattern colors.
  """

  if wide is None:
    wide, tall = common.randint(4, 7), common.randint(4, 7)
    num_colors = common.randint(2, 3)
    while True:
      brow, bcol = common.randint(0, 13 - tall), common.randint(0, 13 - wide)
      prows = [common.randint(1, 11) for _ in range(num_colors)]
      pcols = [common.randint(1, 10) for _ in range(num_colors)]
      if len(set(prows)) != num_colors: continue
      if not common.overlaps([brow] + prows, [bcol] + pcols,
                             [wide] + [2] * num_colors,
                             [tall] + [1] * num_colors, 1): break
    colors = common.shuffle([1, 2, 3, 4, 5, 6, 7, 8, 9])
    bgcolor = colors.pop()
    lefts = [colors.pop() for _ in range(num_colors)]
    rites = [colors.pop() for _ in range(num_colors)]
    while True:
      grid = common.grid(wide, tall, bgcolor)
      for _ in range(2 * len(colors)):
        color = common.choice(rites)
        if common.randint(0, 1):
          length = common.randint(1, wide)
          pos = common.randint(0, wide - length)
          val = common.randint(0, tall - 1)
          for i in range(pos, pos + length):
            grid[val][i] = color
        else:
          length = common.randint(1, tall)
          pos = common.randint(0, tall - length)
          val = common.randint(0, wide - 1)
          for i in range(pos, pos + length):
            grid[i][val] = color
      if len(set(common.flatten(grid))) != num_colors + 1: continue
      # Ensure that each color is connected.
      good = True
      for color in rites:
        pixels = []
        for row in range(tall):
          for col in range(wide):
            if grid[row][col] == color: pixels.append((row, col))
        if not common.connected(pixels): good = False
      if good: break
    pattern = "".join(str(x) for x in common.flatten(grid))

  grid, output = common.grid(13, 13), common.grid(wide, tall)
  cmap = {}
  for prow, pcol, left, rite in zip(prows, pcols, lefts, rites):
    grid[prow][pcol] = left
    grid[prow][pcol + 1] = rite
    cmap[rite] = left
  for i, color in enumerate(pattern):
    c = int(color)
    grid[brow + i // wide][bcol + i % wide] = c
    output[i // wide][i % wide] = cmap[c] if c in cmap.keys() else c
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(wide=7, tall=4, brow=1, bcol=2, prows=[7, 9], pcols=[1, 7],
               lefts=[1, 3], rites=[4, 2],
               pattern="8888888882488882244488888888"),
      generate(wide=7, tall=7, brow=6, bcol=1, prows=[2, 4, 6], pcols=[5, 9, 9],
               lefts=[6, 2, 4], rites=[8, 1, 5],
               pattern="3333333355553333115333811333388883333333333333333"),
      generate(wide=4, tall=4, brow=4, bcol=1, prows=[1, 9], pcols=[6, 7],
               lefts=[2, 3], rites=[4, 8], pattern="1441884188111111"),
      generate(wide=6, tall=6, brow=6, bcol=4, prows=[1, 3], pcols=[1, 1],
               lefts=[2, 1], rites=[3, 4],
               pattern="888888884888844488834388833388888888"),
  ]
  test = [
      generate(wide=5, tall=6, brow=3, bcol=2, prows=[1, 7, 10],
               pcols=[8, 9, 7], lefts=[2, 4, 6], rites=[3, 8, 7],
               pattern="113111333118881177711171111111"),
  ]
  return {"train": train, "test": test}

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


def generate(size=None, line=None, wides=None, talls=None, brows=None,
             bcols=None, pattern=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grids.
    line: The red dividing line.
    wides: The widths of the sprites.
    talls: The heights of the sprites.
    brows: The row offsets of the sprites.
    bcols: The column offsets of the sprites.
    pattern: The pattern of the sprites.
  """

  if size is None:
    size = common.randint(6, 18)
    line = (size + common.randint(-2, 1)) // 2
    max_tall = min(line - 1, size - line - 2)
    bcol = common.randint(1, 2)
    bcols, brows, wides, talls, pattern = [], [], [], [], ""
    while True:
      wide, tall = common.randint(1, 3), common.randint(1, max_tall)
      if bcol + wide > size: break
      bcols.append(bcol)
      wides.append(wide)
      talls.append(tall)
      brows.append(common.randint(0, line - tall))
      sprite = common.grid(wide, tall)
      row, col = common.randint(0, tall - 1), common.randint(0, wide - 1)
      for r in range(tall):
        sprite[r][col] = 1
      for c in range(wide):
        sprite[row][c] = 1
      pattern += "".join(str(x) for x in common.flatten(sprite))
      bcol += wide + common.randint(1, 3)

  grid, output = common.grids(size, size, 8)
  for c in range(size):
    output[line][c] = grid[line][c] = 2
  offset = 0
  for wide, tall, brow, bcol in zip(wides, talls, brows, bcols):
    sprite = common.grid(wide, tall)
    # First, draw the sprite on the input, and store its shape.
    for r in range(tall):
      for c in range(wide):
        sprite[r][c] = int(pattern[offset])
        if sprite[r][c]: grid[brow + r][bcol + c] = 1
        offset += 1
    # Second, process the sprite from the bottom up.
    depth, indexes = 0, []
    for r in range(tall - 1, -1, -1):
      count = 0
      for c in range(wide):
        if not sprite[r][c]: continue
        count += 1
        if r == tall - 1: indexes.append(c)
      if count > 1: break
      depth += 1
    # Third, figure out what on earth to do with this thing.
    depth = (size - tall) if depth == tall else (line - tall + depth)
    if len(indexes) == 1: output[line][bcol + indexes[0]] = 8
    for r in range(tall):
      for c in range(wide):
        if sprite[r][c]: output[depth + r][bcol + c] = 1
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=9, line=5, wides=[1, 1, 2], talls=[1, 2, 1],
               brows=[1, 1, 2], bcols=[1, 3, 7], pattern="11111"),
      generate(size=7, line=3, wides=[1], talls=[1], brows=[0], bcols=[2],
               pattern="1"),
      generate(size=11, line=6, wides=[3, 1, 1], talls=[3, 3, 1],
               brows=[1, 1, 0], bcols=[1, 7, 9], pattern="1111001001111"),
  ]
  test = [
      generate(size=18, line=8, wides=[3, 3, 2, 1, 1], talls=[5, 5, 4, 7, 1],
               brows=[1, 1, 2, 0, 2], bcols=[2, 6, 10, 14, 17], 
               pattern="0100100100101111110100100100100111010111111111"),
  ]
  return {"train": train, "test": test}

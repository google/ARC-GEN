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
             bcol=None, lrow=None, lcol=None, bgcolor=None, colors=None,
             pattern=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: Width of the input grid.
    height: Height of the input grid.
    wide: Width of the pattern.
    tall: Height of the pattern.
    brow: Row of the pattern's upper left corner.
    bcol: Column of the pattern's upper left corner.
    lrow: Row of the legend's upper left corner.
    lcol: Column of the legend's upper left corner.
    bgcolor: Background color.
    colors: Colors of the legend.
    pattern: Pattern of the sprite.
  """

  if width is None:
    while True:
      width, height = common.randint(10, 20), common.randint(10, 20)
      wide = common.randint(width // 3, 2 * width // 3)
      tall = common.randint(height // 3, 2 * height // 3)
      brow = common.randint(0, height - tall)
      bcol = common.randint(0, width - wide)
      lrow = common.randint(0, height - 3)
      lcol = common.randint(0, width - wide)
      if not common.overlaps([brow, lrow], [bcol, lcol], [wide, wide], [tall, 3], 1):
        break
    bgcolor = common.random_color(exclude=[5])
    colors = []
    for _ in range(wide):
      if colors and common.randint(0, 3) == 0:
        colors.append(colors[-1])
      else:
        colors.append(common.random_color(exclude=[5, bgcolor]))
    while True:
      pattern = common.grid(wide, tall)
      while common.flatten(pattern).count(1) < wide * tall // 2:
        if common.randint(0, 1):
          length = common.randint(1, wide // 2)
          pos = common.randint(0, wide - length)
          val = common.randint(0, tall - 1)
          for i in range(length):
            pattern[val][pos + i] = 1
        else:
          length = common.randint(1, tall // 2)
          pos = common.randint(0, tall - length)
          val = common.randint(0, wide - 1)
          for i in range(length):
            pattern[pos + i][val] = 1
      pixels = []
      min_row, max_row, min_col, max_col = tall, -1, wide, -1
      for row in range(tall):
        for col in range(wide):
          if not pattern[row][col]: continue
          pixels.append((row, col))
          min_row, max_row = min(min_row, row), max(max_row, row)
          min_col, max_col = min(min_col, col), max(max_col, col)
      if min_row > 0 or max_row < tall - 1 or min_col > 0 or max_col < wide - 1:
        continue
      if common.connected(pixels): break
    pattern = "".join(str(x) for x in common.flatten(pattern))

  grid, output = common.grid(width, height), common.grid(wide, tall, bgcolor)
  for row in range(tall):
    for col in range(wide):
      if pattern[row * wide + col] == "0": continue
      grid[brow + row][bcol + col] = 5
      output[row][col] = colors[col]
  for row in range(3):
    for col in range(wide):
      grid[lrow + row][lcol + col] = colors[col] if row < 2 else bgcolor
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=10, height=15, wide=5, tall=6, brow=1, bcol=2, lrow=9,
               lcol=1, bgcolor=8, colors=[4, 2, 3, 4, 4],
               pattern="111001010000111111010100101111"),
      generate(width=15, height=15, wide=7, tall=10, brow=4, bcol=6, lrow=0,
               lcol=0, bgcolor=6, colors=[2, 2, 1, 3, 3, 4, 8],
               pattern="1001101111111100110001111111110101001011110101111111111100011101111011"),
      generate(width=16, height=15, wide=8, tall=5, brow=3, bcol=2, lrow=11,
               lcol=1, bgcolor=1, colors=[3, 3, 2, 8, 8, 8, 6, 6],
               pattern="1011111111010001011110110100001101111111"),
  ]
  test = [
      generate(width=18, height=18, wide=10, tall=7, brow=5, bcol=1, lrow=0,
               lcol=8, bgcolor=9, colors=[2, 4, 4, 4, 8, 8, 3, 3, 6, 6],
               pattern="0110010111111111111100101100111111100010010010011001111111110011000011"),
  ]
  return {"train": train, "test": test}

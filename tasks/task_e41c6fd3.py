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


def generate(width=None, height=None, wide=None, tall=None, brows=None,
             bcols=None, bcolors=None, pattern=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grids.
    height: The height of the grids.
    wide: The width of the blocks.
    tall: The height of the blocks.
    brows: The row indices of the blocks.
    bcols: The column indices of the blocks.
    bcolors: The colors of the blocks.
    pattern: The pattern of the blocks.
  """

  if width is None:
    width, height = common.randint(20, 30), common.randint(12, 18)
    wide, tall = common.randint(4, 6), common.randint(4, 6)
    num_boxes = common.randint(3, (width - 1) // wide)
    bcolors = common.random_colors(num_boxes, exclude=[8])
    bcolors[0] = 8
    while True:
      brows = [common.randint(0, height - tall) for _ in range(num_boxes)]
      if len(set(brows)) == num_boxes: break
    while True:
      bcols = [common.randint(0, width - wide) for _ in range(num_boxes)]
      if not common.overlaps_1d(bcols, [wide] * num_boxes): break
    while True:
      sprite = common.grid(wide, tall)
      for row in range(tall):
        for col in range(wide):
          if common.randint(0, 2): continue
          sprite[row][col] = sprite[row][wide - 1 - col] = 1
      pixels = []
      min_row, max_row, min_col, max_col = tall, -1, wide, -1
      for row in range(tall):
        for col in range(wide):
          if not sprite[row][col]: continue
          pixels.append((row, col))
          min_row, max_row = min(min_row, row), max(max_row, row)
          min_col, max_col = min(min_col, col), max(max_col, col)
      if min_row > 0 or max_row < tall - 1 or min_col > 0 or max_col < wide - 1:
        continue
      if 0 in common.flatten(sprite) and common.connected(pixels): break
    pattern = "".join(str(x) for x in common.flatten(sprite))

  grid, output = common.grids(width, height)
  for brow, bcol, bcolor in zip(brows, bcols, bcolors):
    for r in range(tall):
      for c in range(wide):
        if pattern[r * wide + c] == "0": continue
        grid[brow + r][bcol + c] = bcolor
        output[brows[0] + r][bcol + c] = bcolor
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=30, height=14, wide=6, tall=4, brows=[6, 10, 2, 8],
               bcols=[4, 12, 18, 24], bcolors=[8, 6, 1, 3],
               pattern="001100101101111111110011"),
      generate(width=23, height=13, wide=4, tall=5, brows=[1, 3, 7],
               bcols=[10, 3, 16], bcolors=[8, 2, 4],
               pattern="01101111111111111001"),
      generate(width=30, height=16, wide=4, tall=4, brows=[2, 3, 5, 7, 8],
               bcols=[13, 24, 2, 17, 7], bcolors=[8, 3, 1, 2, 4],
               pattern="0110111101101111"),
  ]
  test = [
      generate(width=30, height=17, wide=5, tall=5, brows=[7, 2, 9, 12],
               bcols=[21, 14, 2, 9], bcolors=[8, 4, 3, 1],
               pattern="1111100100011101111100100"),
  ]
  return {"train": train, "test": test}

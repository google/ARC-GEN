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


def generate(size=None, hcolors=None, brows=None, values=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the sprites.
    hcolors: The colors of the horizontal boxes.
    brows: The rows of the filled boxes
    values: The values of the sprites.
  """

  if size is None:
    size = common.randint(2, 5)
    width = common.randint(3, 4 if size < 5 else 3)
    hcolors = common.sample([3, 4, 6, 7], width)
    brows = [common.randint(0, 2) for _ in range(width)]
    values = []
    for _ in range(width):
      while True:
        value = [common.randint(0, 1) for _ in range(size * size)]
        if sum(value) > 0 and sum(value) < size * size: break
      values.extend(value)
    values = "".join(str(v) for v in values)

  vcolors = [5, 9, 0]
  inwidth = len(hcolors) * (size + 3) + 1
  inheight = len(vcolors) * (size + 3) + 1
  outwidth, outheight = inwidth - 2, size + 2
  grid = common.grid(inwidth, inheight, 8)
  output = common.grid(outwidth, outheight, 8)
  # Draw the input left column legend.
  for row, vcolor in enumerate(vcolors):
    for r in range(size + 2):
      grid[(size + 3) * row + r + 1][0] = vcolor
  # Draw the input blue boxes.
  for row in range(len(vcolors)):
    for col in range(len(hcolors)):
      r, c = row * (size + 3) + 1, col * (size + 3) + 1
      common.hollow_rect(grid, size + 2, size + 2, r, c, 1)
  # Draw the input red sprites.
  for row in range(len(vcolors)):
    for col in range(len(hcolors)):
      for scol in range(size):
        for srow in range(size):
          r, c = row * (size + 3) + 2 + srow, col * (size + 3) + 2 + scol
          color = int(values[col * (size * size) + srow * size + scol])
          if color: grid[r][c] = 2
  # Draw the input solid colors.
  for col, (hcolor, brow) in enumerate(zip(hcolors, brows)):
    r, c = brow * (size + 3) + 2, col * (size + 3) + 2
    common.rect(grid, size, size, r, c, hcolor)
  # Draw the output boxes and sprites.
  for col, (hcolor, brow) in enumerate(zip(hcolors, brows)):
    r, c = 0, col * (size + 3)
    common.hollow_rect(output, size + 2, size + 2, r, c, vcolors[brow])
    for scol in range(size):
      for srow in range(size):
        r, c = 1 + srow, col * (size + 3) + 1 + scol
        color = int(values[col * (size * size) + srow * size + scol])
        if color: output[r][c] = hcolor
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=3, hcolors=[3, 6, 7], brows=[1, 0, 0], values="010111010100110011111010000"),
      generate(size=4, hcolors=[4, 3, 7, 6], brows=[2, 1, 1, 2], values="1000111000100111001011110101011111100010011100101110101110011001"),
  ]
  test = [
      generate(size=5, hcolors=[6, 4, 3], brows=[1, 2, 0], values="001000111000100111110010001000111100001001111000100001100011011001110001000"),
  ]
  return {"train": train, "test": test}

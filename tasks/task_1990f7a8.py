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


def generate(width=None, height=None, brows=None, bcols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    colors: The contents of the boxes.
  """

  if width is None:
    base = common.randint(16, 24)
    width, height = base + common.randint(-1, 1), base + common.randint(-1, 1)
    row, col = common.randint(4, height - 5), common.randint(4, width - 5)
    brows, bcols = [], []
    brows.append(common.randint(1, row - 3))
    bcols.append(common.randint(1, col - 3))
    brows.append(common.randint(1, row - 3))
    bcols.append(common.randint(col + 1, width - 4))
    brows.append(common.randint(row + 1, height - 4))
    bcols.append(common.randint(1, col - 3))
    brows.append(common.randint(row + 1, height - 4))
    bcols.append(common.randint(col + 1, width - 4))
    colors = []
    for _ in range(4):
      while True:
        row, col = common.conway_sprite(3, 3, common.randint(0, 5))
        pixels = list(zip(row, col))
        if common.diagonally_connected(pixels): break
      for r in range(3):
        for c in range(3):
          colors.append(1 if (r, c) in pixels else 0)
    colors = "".join([str(color) for color in colors])

  grid, output = common.grid(width, height), common.grid(7, 7)
  for row in range(2):
    for col in range(2):
      brow, bcol = brows[row * 2 + col], bcols[row * 2 + col]
      for r in range(3):
        for c in range(3):
          color = int(colors[row * 18 + col * 9 + r * 3 + c])
          if not color: continue
          output[row * 4 + r][col * 4 + c] = grid[brow + r][bcol + c] = 2
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=19, height=17, brows=[2, 2, 9, 8], bcols=[3, 11, 6, 13],
               colors="101011001110101110111101111110010101"),
      generate(width=23, height=23, brows=[2, 5, 12, 13], bcols=[3, 11, 5, 16],
               colors="111101111111111111101010111100011100"),
      generate(width=16, height=17, brows=[1, 2, 12, 8], bcols=[1, 8, 3, 10],
               colors="010101010101010110101110001010111010"),
  ]
  test = [
      generate(width=17, height=17, brows=[2, 4, 11, 11], bcols=[6, 12, 1, 10],
               colors="101010111001011101101111100111101101"),
  ]
  return {"train": train, "test": test}

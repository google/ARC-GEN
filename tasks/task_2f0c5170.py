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


def generate(width=None, height=None, wide=None, tall=None, bwides=None,
             btalls=None, irows=None, icols=None, orows=None, ocols=None,
             colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the input grid.
    height: The height of the input grid.
    wide: The width of the sprite.
    tall: The height of the sprite.
    bwides: The widths of the two rectangles.
    btalls: The heights of the two rectangles.
    irows: The rows of the input rectangles.
    icols: The columns of the input rectangles.
    orows: The rows of the sprite in the rectangles.
    ocols: The columns of the sprite in the rectangles.
    colors: The colors of the sprite.
  """

  if width is None:
    base = common.randint(19, 21)
    width, height = base + common.randint(-2, 2), base + common.randint(-2, 2)
    wide, tall = common.randint(3, 5), common.randint(3, 5)
    # Choose the box sizes and locations.
    while True:
      bwides = [wide + common.randint(0, wide) for _ in range(2)]
      btalls = [tall + common.randint(0, tall) for _ in range(2)]
      irows = [common.randint(1, height - btall - 1) for btall in btalls]
      icols = [common.randint(1, width - bwide - 1) for bwide in bwides]
      if not common.overlaps(irows, icols, bwides, btalls, 1): break
    # Choose the sprite locations.
    orows = [common.randint(0, btall - tall) for btall in btalls]
    ocols = [common.randint(0, bwide - wide) for bwide in bwides]
    # Choose the sprite contents
    pixels = common.connected_sprite(wide, tall)
    colors = []
    for r in range(tall):
      for c in range(wide):
        colors.append(4 if (r, c) in pixels else 0)
    pixel = common.choice(pixels)
    colors[pixel[0] * wide + pixel[1]] = common.randint(1, 3)

  grid = common.grid(width, height, 8)
  output = common.grid(bwides[1], btalls[1])
  for bwide, btall, irow, icol in zip(bwides, btalls, irows, icols):
    common.rect(grid, bwide, btall, irow, icol, 0)
  for r in range(tall):
    for c in range(wide):
      color = colors[r * wide + c]
      grid[irows[0] + orows[0] + r][icols[0] + ocols[0] + c] = color
      if color not in [0, 4]:
        grid[irows[1] + orows[1] + r][icols[1] + ocols[1] + c] = color
      output[orows[1] + r][ocols[1] + c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=22, height=21, wide=4, tall=3, bwides=[6, 5],
               btalls=[4, 5], irows=[12, 1], icols=[2, 11], orows=[1, 0],
               ocols=[1, 1], colors=[0, 4, 4, 0, 4, 4, 2, 4, 0, 4, 4, 0]),
      generate(width=23, height=20, wide=3, tall=4, bwides=[6, 9],
               btalls=[7, 9], irows=[10, 2], icols=[15, 2], orows=[2, 3],
               ocols=[1, 2], colors=[0, 4, 0, 4, 4, 4, 3, 4, 0, 4, 4, 4]),
      generate(width=18, height=19, wide=5, tall=4, bwides=[7, 7],
               btalls=[4, 8], irows=[2, 9], icols=[2, 8], orows=[0, 1],
               ocols=[1, 2],
               colors=[0, 0, 0, 4, 0, 0, 4, 4, 4, 0, 4, 4, 1, 4, 4, 0, 4, 4, 0, 0]),
  ]
  test = [
      generate(width=19, height=19, wide=5, tall=3, bwides=[7, 9],
               btalls=[5, 7], irows=[4, 11], icols=[1, 7], orows=[1, 4],
               ocols=[1, 1],
               colors=[4, 4, 0, 4, 4, 0, 4, 2, 4, 0, 4, 4, 4, 4, 4]),
  ]
  return {"train": train, "test": test}

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


def generate(width=None, height=None, brow=None, bcol=None, prow=None,
             pcol=None, colors=None, pattern=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
  """

  def draw():
    grid, output = common.grid(width, height), common.grid(3 * len(colors), 3)
    # Draw the sprite.
    for j, color in enumerate(pattern):
      grid[brow + j // 3][bcol + j % 3] = color
    # Check that the legend won't overlap the sprite.
    for row in range(prow - 1, prow + 2):
      for col in range(pcol - 1, pcol + 2 * len(colors)):
        if common.get_pixel(grid, row, col) not in [0, -1]: return None, None
    # Draw the legend & output.
    for i, icolor in enumerate(colors):
      grid[prow][pcol + i * 2] = icolor
      for j, jcolor in enumerate(pattern):
        output[j // 3][i * 3 + j % 3] = icolor * jcolor
    if xpose: grid, output = common.transpose(grid), common.transpose(output)
    return grid, output

  if width is None:
    width, height = common.randint(8, 16), common.randint(8, 16)
    pixels = common.diagonally_connected_sprite(3, 3, common.randint(2, 5))
    pattern = []
    for row in range(3):
      for col in range(3):
        pattern.append(1 if (row, col) in pixels else 0)
    colors = common.random_colors(common.randint(2, 4), exclude=[1])
    xpose = common.randint(0, 1)
    while True:
      brow = common.randint(0, height - 3)
      bcol = common.randint(0, width - 3)
      prow = common.randint(1, height - 2)
      pcol = common.randint(1, width - 2 * len(colors))
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=11, height=11, brow=2, bcol=2, prow=7, pcol=1,
               colors=[6, 2], pattern=[0, 1, 0, 1, 1, 0, 0, 0, 1], xpose=True),
      generate(width=11, height=9, brow=0, bcol=4, prow=5, pcol=1,
               colors=[3, 6, 8], pattern=[0, 1, 0, 1, 1, 1, 1, 1, 0],
               xpose=True),
      generate(width=10, height=11, brow=0, bcol=1, prow=6, pcol=1,
               colors=[3, 2], pattern=[0, 1, 1, 1, 1, 0, 0, 1, 1], xpose=False),
      generate(width=14, height=11, brow=1, bcol=1, prow=7, pcol=4,
               colors=[2, 3, 4], pattern=[1, 0, 1, 0, 1, 0, 1, 1, 1],
               xpose=False),
  ]
  test = [
      generate(width=9, height=11, brow=3, bcol=0, prow=1, pcol=2,
               colors=[7, 6, 3, 2], pattern=[0, 1, 0, 1, 1, 1, 0, 1, 0],
               xpose=True),
      generate(width=11, height=11, brow=1, bcol=0, prow=6, pcol=2,
               colors=[2, 8, 3, 6], pattern=[0, 1, 1, 1, 1, 0, 1, 1, 0],
               xpose=False),
  ]
  return {"train": train, "test": test}

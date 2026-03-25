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


def generate(width=None, height=None, size=None, scale=None, brow=None,
             bcol=None, srow=None, scol=None, rotate=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    size: The size of the sprite.
    scale: The scale of the sprite.
    brow: The row of the box.
    bcol: The column of the box.
    srow: The row of the sprite.
    scol: The column of the sprite.
    rotate: Whether to rotate the grids.
    colors: The colors of the sprite.
  """

  if width is None:
    size = common.randint(3, 4)
    scale = 2 if size == 4 else common.randint(3, 4)
    length = size * scale
    width = length + common.randint(3, 5)
    height = 12 + length + common.randint(0, 4)
    brow, bcol = common.randint(1, 3), common.randint(1, width - size - 2)
    srow = common.randint(10, height - 1 - length)
    scol = common.randint(1, width - 1 - length)
    pixels = common.diagonally_connected_sprite(size, size)
    colors = []
    for r in range(size):
      for c in range(size):
        colors.append(common.choice([1, 2, 3, 4]) if (r, c) in pixels else 0)
    rotate = common.randint(0, 3)

  grid, output = common.grids(width, height)
  for row in range(size):
    for col in range(size):
      color = colors[row * size + col]
      if not color: continue
      output[brow + row][bcol + col] = grid[brow + row][bcol + col] = color
      for r in range(scale):
        for c in range(scale):
          rr, cc = srow + col * scale + r, scol + (size - 1 - row) * scale + c
          grid[rr][cc], output[rr][cc] = 8, color
  for _ in range(rotate):
    grid, output = common.flip(grid), common.flip(output)
    grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=12, height=22, size=3, scale=3, brow=3, bcol=3, srow=10,
               scol=1, rotate=0, colors=[0, 3, 1, 4, 3, 0, 2, 0, 4]),
      generate(width=13, height=24, size=4, scale=2, brow=1, bcol=2, srow=12,
               scol=2, rotate=0,
               colors=[0, 0, 3, 0, 2, 0, 3, 4, 2, 1, 1, 0, 2, 0, 0, 4]),
  ]
  test = [
      generate(width=16, height=26, size=3, scale=4, brow=2, bcol=6, srow=12,
               scol=3, rotate=1, colors=[0, 2, 2, 4, 4, 0, 0, 0, 3]),
  ]
  return {"train": train, "test": test}

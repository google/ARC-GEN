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


def generate(width=None, height=None, length=None, brow=None, bcol=None,
             prow=None, pcol=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    length: The length of the square shapes.
    brow: The row of the big grid.
    bcol: The column of the big grid.
    prow: The row of the legend.
    pcol: The column of the legend.
    colors: A list of colors to use.
  """

  def draw():
    grid, output = common.grids(width, height)
    # Draw the big grid of shapes.
    for row in range(length):
      for col in range(length):
        color = colors[row * length + col]
        if not color: continue
        for r in range(length):
          for c in range(length):
            if not colors[r * length + c]: continue
            rr = brow + (length + 1) * row + r
            cc = bcol + (length + 1) * col + c
            grid[rr][cc], output[rr][cc] = 1, color
    # Check that the legend space is open.
    for r in range(prow - 1, prow + length + 1):
      for c in range(pcol - 1, pcol + length + 1):
        if common.get_pixel(grid, r, c) not in [-1, 0]: return None, None
    # Draw the legend.
    for row in range(length):
      for col in range(length):
        color = colors[row * length + col]
        output[prow + row][pcol + col] = grid[prow + row][pcol + col] = color
    return grid, output

  if width is None:
    length = common.randint(2, 3)
    hues = common.random_colors(common.randint(2, length + 1), exclude=[1])
    # Choose the sprite and sprite colors
    while True:
      pixels = common.diagonally_connected_sprite(length, length, length)
      colors = []
      for r in range(length):
        for c in range(length):
          colors.append(common.choice(hues) if (r, c) in pixels else 0)
      if len(set(colors)) == len(hues) + 1: break
    # Choose the locations
    while True:
      grid_size = length * (length + 1)
      width = grid_size + common.randint(0, 7)
      height = grid_size + common.randint(0, 7)
      brow = common.randint(0, height - grid_size)
      bcol = common.randint(0, width - grid_size)
      prow = common.randint(0, height - length)
      pcol = common.randint(0, width - length)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=12, height=10, length=2, brow=1, bcol=5, prow=3, pcol=1,
               colors=[2, 4, 3, 0]),
      generate(width=18, height=12, length=3, brow=0, bcol=0, prow=2, pcol=14,
               colors=[2, 3, 0, 3, 0, 3, 0, 3, 2]),
  ]
  test = [
      generate(width=12, height=14, length=3, brow=2, bcol=1, prow=0, pcol=0,
               colors=[0, 2, 0, 4, 7, 4, 3, 0, 3]),
  ]
  return {"train": train, "test": test}

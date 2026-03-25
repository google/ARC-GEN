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


def generate(width=None, height=None, brows=None, bcols=None, bcolors=None,
             colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    brows: The rows of the squares.
    bcols: The columns of the squares.
    bcolors: The colors of the squares.
    colors: The colors of the background.
  """

  def draw():
    grid, output = common.grids(width, height)
    for i, color in enumerate(colors):
      output[i // width][i % width] = grid[i // width][i % width] = color
    # Check that boxes aren't adjacent to their same color.
    for brow, bcol, bcolor in zip(brows, bcols, bcolors):
      for r in range(brow - 1, brow + 4):
        for c in range(bcol - 1, bcol + 4):
          if common.get_pixel(grid, r, c) == bcolor: return None, None
    # Draw boxes.
    for brow, bcol, bcolor in zip(brows, bcols, bcolors):
      for r in range(height):
        output[r][bcol + 1] = 0 if r - 1 in brows else bcolor
      for c in range(width):
        output[brow + 1][c] = 0 if c - 1 in bcols else bcolor
      common.rect(grid, 3, 3, brow, bcol, bcolor)
      common.rect(output, 3, 3, brow, bcol, bcolor)
    return grid, output

  if width is None:
    base = common.randint(14, 18)
    width = base + common.randint(-2, 2)
    height = base + common.randint(-2, 2)
    num_boxes = 1
    if base >= 15: num_boxes = 2
    if base >= 17: num_boxes = 3
    bcolors = common.random_colors(num_boxes)
    while True:
      brows = [common.randint(0, height - 3) for _ in range(num_boxes)]
      bcols = [common.randint(0, width - 3) for _ in range(num_boxes)]
      if common.overlaps_1d(brows, [3] * num_boxes): continue
      if common.overlaps_1d(bcols, [3] * num_boxes): continue
      colors = [common.randint(0, 9) for _ in range(width * height)]
      colors = [0 if color else common.random_color() for color in colors]
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=14, height=18, brows=[4, 7], bcols=[10, 3], bcolors=[2, 3],
               colors=[0, 0, 0, 0, 0, 0, 8, 7, 0, 0, 0, 0, 0, 0,
                       6, 8, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 6, 0, 1, 0, 0, 0, 0,
                       0, 0, 2, 6, 5, 0, 3, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0,
                       0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       5, 0, 0, 0, 0, 0, 3, 0, 4, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 1,
                       0, 0, 0, 8, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 8, 0, 6, 7, 0, 0, 0, 0, 0, 0, 0, 8]),
      generate(width=13, height=14, brows=[5], bcols=[5], bcolors=[4],
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 3, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0,
                       0, 0, 0, 0, 9, 0, 0, 6, 0, 0, 0, 0, 0,
                       7, 0, 0, 0, 3, 1, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       9, 7, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0,
                       0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 1, 0, 0,
                       0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 8, 0]),
      generate(width=18, height=18, brows=[2, 9, 14], bcols=[11, 3, 15],
               bcolors=[8, 6, 3],
               colors=[0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 1, 3, 0, 0,
                       0, 0, 4, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0,
                       1, 0, 0, 7, 0, 0, 0, 7, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       8, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0,
                       0, 5, 0, 0, 0, 8, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0,
                       0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       1, 3, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 4, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 4, 0, 0, 0, 0]),
      generate(width=18, height=17, brows=[4, 10], bcols=[6, 12],
               bcolors=[8, 7],
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0,
                       0, 0, 1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9,
                       0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0,
                       0, 5, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0,
                       0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 4,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
  ]
  test = [
      generate(width=19, height=19, brows=[2, 7, 12], bcols=[6, 13, 0],
               bcolors=[4, 8, 7],
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 2, 0, 0,
                       4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0,
                       1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0,
                       0, 5, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0,
                       0, 0, 7, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 4,
                       0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 5, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 2, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 4, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 6, 0, 0, 0, 2, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 6, 6, 9, 9, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 2, 0,
                       3, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 4, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0]),
  ]
  return {"train": train, "test": test}

# Copyright 2025 Google LLC
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


def generate(width=None, rows=None, cols=None, colors=None, quadrant=None,
             height=2, size=9):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid in *quadrants*
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    quadrant: which quadrant of the input grid to fill
    height: the height of the input grid in *quadrants*
    size: the width and height of the (square) grid
  """
  if rows is None:
    width = common.randint(1, 3)
    pixels = common.random_pixels(size, size, 0.125)
    rows, cols = zip(*pixels)
    color_list = common.random_colors(common.randint(3, 4),
                                      exclude=[common.yellow()])
    idxs = [common.randint(0, len(color_list) - 1) for _ in range(len(pixels))]
    colors = [color_list[i] for i in idxs]
    quadrant = common.randint(0, width * height - 1)

  grid = common.grid(width * (size + 1) - 1, height * (size + 1) - 1)
  output = common.grid(width * (size + 1) - 1, height * (size + 1) - 1)
  for r in range(height * (size + 1) - 1):
    for c in range(width * (size + 1) - 1):
      if r % (size + 1) != size and c % (size + 1) != size: continue
      output[r][c] = grid[r][c] = common.yellow()
  for h in range(height):
    for w in range(width):
      for r, c, color in zip(rows, cols, colors):
        output[h * (size + 1) + r][w * (size + 1) + c] = color
        if h * width + w != quadrant: continue
        grid[h * (size + 1) + r][w * (size + 1) + c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=2, rows=[1, 2, 3, 4, 4, 6, 6, 7, 7, 8],
               cols=[5, 3, 2, 1, 5, 3, 4, 4, 7, 1],
               colors=[7, 2, 2, 3, 3, 8, 7, 8, 3, 7], quadrant=2),
      generate(width=1, rows=[1, 1, 2, 4, 5, 6, 6, 7, 7, 7],
               cols=[5, 7, 2, 4, 2, 2, 7, 1, 5, 6],
               colors=[5, 2, 1, 1, 1, 2, 2, 2, 5, 5],
               quadrant=0),
  ]
  test = [
      generate(width=3, rows=[1, 2, 2, 3, 3, 4, 6, 8],
               cols=[4, 1, 7, 1, 7, 4, 2, 6],
               colors=[3, 2, 2, 3, 2, 2, 6, 6], quadrant=1),
  ]
  return {"train": train, "test": test}

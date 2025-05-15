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


def generate(height=None, rows=None, cols=None, colors=None, width=13):
  """Returns input and output grids according to the given parameters.

  Args:
    height: the height of the grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    width: the width of the grid
  """
  if height is None:
    wide, tall = common.randint(7, 9), common.randint(7, 9)
    height = tall + common.randint(2, 5)
    top, cutline = common.randint(1, height - tall - 1), common.randint(0, 2)
    horiz = None if cutline != 1 else common.randint(top + 2, top + tall - 3)
    vert = None if cutline != 2 else common.randint(4, wide - 1)
    pixels = []
    for r in range(height):
      for c in range(width):
        # Skip outside cells, and inside cells that aren't part of the cutline
        if r < top or r >= top + tall or c < 2 or c >= wide + 2: continue
        if r > top and r < top + tall - 1 and c > 2 and c < wide + 1:
          if r != horiz and c != vert: continue
        pixels.append((r, c))
    rows, cols = zip(*pixels)
    colors = [
        common.blue() if common.randint(0, 3) else common.red() for _ in pixels
    ]

  grid, output = common.grids(width, height)
  for r, c, color in zip(rows, cols, colors):
    if color == common.blue():
      grid[r][c] = color
    output[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(height=9,
               rows=[1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7,
                     7, 7, 7, 7, 7, 7, 7, 7],
               cols=[2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 10, 2, 10, 2, 10, 2, 10, 2,
                     10, 2, 3, 4, 5, 6, 7, 8, 9, 10],
               colors=[1, 2, 1, 2, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2, 2, 1, 1, 1,
                       1, 1, 2, 2, 1, 1, 2, 1, 1]),
      generate(height=11,
               rows=[2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7,
                     7, 7, 8, 8, 8, 8, 8, 8, 8],
               cols=[2, 3, 4, 5, 6, 7, 8, 2, 4, 8, 2, 4, 8, 2, 4, 8, 2, 4, 8, 2,
                     4, 8, 2, 3, 4, 5, 6, 7, 8],
               colors=[1, 1, 1, 2, 2, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1,
                       2, 1, 1, 1, 1, 1, 1, 2, 1, 2]),
      generate(height=13,
               rows=[3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 7, 7, 7,
                     7, 7, 7, 7, 8, 8, 9, 9, 10, 10, 10, 10, 10, 10, 10, 10,
                     10],
               cols=[2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 10, 2, 10, 2, 10, 2, 3, 4,
                     5, 6, 7, 8, 9, 10, 2, 10, 2, 10, 2, 3, 4, 5, 6, 7, 8, 9,
                     10],
               colors=[1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1,
                       2, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1]),
  ]
  test = [
      generate(height=13,
               rows=[2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 7,
                     7, 7, 7, 7, 7, 7, 8, 8, 9, 9, 10, 10, 10, 10, 10, 10, 10,
                     10, 10],
               cols=[2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 10, 2, 10, 2, 10, 2, 10, 2,
                     3, 4, 5, 6, 7, 8, 9, 10, 2, 10, 2, 10, 2, 3, 4, 5, 6, 7, 8,
                     9, 10],
               colors=[1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 2,
                       1, 2, 1, 2, 2, 1, 1, 2, 2, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1,
                       1]),
  ]
  return {"train": train, "test": test}

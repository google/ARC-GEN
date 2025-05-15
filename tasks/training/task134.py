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


def generate(width=None, height=None, rows=None, cols=None, megarows=None,
             megacols=None, rowoffset=None, coloffset=None, color=None,
             megacolor=None, magnifier=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    megarows: a list of vertical coordinates for the mega sprite
    megacols: a list of horizontal coordinates for the mega sprite
    rowoffset: a vertical offset for the mega sprite
    coloffset: a horizontal offset for the mega sprite
    color: a digit representing a color to be used
    megacolor: a digit representing a color to be used for the mega sprite
    magnifier: the amount to magnify the sprite
  """
  if width is None:
    width, height = common.randint(20, 30), common.randint(20, 30)
    pixels = common.random_pixels(width, height, 0.05)
    rows, cols = zip(*pixels)
    megarows, megacols = common.conway_sprite()
    magnifier = common.randint(2, 6)
    rowoffset = common.randint(1, height - 3 * magnifier)
    coloffset = common.randint(1, width - 3 * magnifier)
    color = common.random_color()
    megacolor = common.random_color(exclude=[color])

  grid, output = common.grid(width, height), common.grid(3, 3)
  for r, c in zip(rows, cols):
    grid[r][c] = color
  for row, col in zip(megarows, megacols):
    for dr in range(magnifier):
      for dc in range(magnifier):
        r = rowoffset + row * magnifier + dr
        c = coloffset + col * magnifier + dc
        grid[r][c] = megacolor
    output[row][col] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=24, height=20,
               rows=[0, 0, 0, 1, 1, 2, 2, 2, 3, 3, 5, 8, 8, 9, 9, 10, 11, 11,
                     11, 12, 13, 14, 14, 14, 15, 15, 17, 17, 17, 17, 19, 19, 19,
                     19, 19, 19],
               cols=[9, 10, 23, 10, 21, 1, 18, 20, 7, 21, 17, 15, 18, 11, 23,
                     15, 19, 20, 22, 17, 19, 0, 17, 20, 15, 16, 12, 16, 20, 22,
                     0, 1, 3, 5, 10, 18],
               megarows=[0, 0, 1, 2, 2, 2], megacols=[0, 2, 1, 0, 1, 2],
               rowoffset=3, coloffset=3,
               color=8, megacolor=4, magnifier=4),
      generate(width=23, height=22,
               rows=[0, 1, 1, 2, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 8, 8, 9, 9, 9,
                     10, 10, 10, 11, 12, 12, 12, 13, 14, 14, 15, 15, 17, 20, 20,
                     20, 21, 21],
               cols=[2, 5, 21, 5, 1, 1, 2, 20, 8, 10, 12, 18, 1, 9, 11, 7, 22,
                     6, 15, 16, 0, 12, 21, 15, 4, 5, 10, 19, 9, 15, 11, 19, 10,
                     7, 10, 13, 4, 11],
               megarows=[0, 0, 1, 2], megacols=[0, 2, 1, 0],
               rowoffset=1, coloffset=10,
               color=2, megacolor=1, magnifier=3),
      generate(width=23, height=24,
               rows=[0, 1, 1, 2, 3, 3, 4, 6, 8, 10, 11, 12, 12, 15, 17, 18, 23],
               cols=[1, 6, 15, 0, 4, 13, 10, 21, 15, 3, 3, 18, 22, 19, 8, 8,
                     21],
               megarows=[0, 1, 1, 2, 2], megacols=[1, 1, 2, 0, 2],
               rowoffset=5, coloffset=2,
               color=3, megacolor=6, magnifier=5),
  ]
  test = [
      generate(width=26, height=22,
               rows=[0, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 4, 6, 7, 7, 7, 9, 9,
                     9, 11, 12, 12, 12, 13, 13, 14, 14, 14, 15, 15, 15, 15, 15,
                     16, 16, 16, 16, 16, 16, 17, 18, 18, 18, 18, 18, 19, 19, 21,
                     21, 21, 21],
               cols=[21, 3, 10, 23, 8, 13, 18, 19, 20, 21, 4, 9, 12, 19, 22, 14,
                     21, 23, 15, 16, 24, 1, 1, 4, 9, 2, 25, 0, 8, 19, 2, 5, 17,
                     19, 25, 1, 3, 4, 9, 11, 16, 17, 4, 13, 16, 21, 25, 8, 11,
                     11, 14, 15, 20],
               megarows=[0, 0, 1, 1, 2], megacols=[0, 2, 1, 2, 2],
               rowoffset=4, coloffset=2,
               color=4, megacolor=8, magnifier=4),
  ]
  return {"train": train, "test": test}

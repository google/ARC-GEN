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


def generate(width=None, height=None, rows=None, cols=None, wide=None,
             tall=None, brow=None, bcol=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    wide: the width of the box
    tall: the height of the box
    brow: the row where the box is placed
    bcol: the column where the box is placed
    colors: a list of two colors, one for the sprite and one for the box
  """
  if width is None:
    wide, tall = common.randint(3, 10), common.randint(3, 10)
    width = common.randint(4 + wide, 4 + wide * 2)
    height = common.randint(4 + tall, 4 + tall * 2)
    brow = common.randint(2, height - tall - 2)
    bcol = common.randint(2, width - wide - 2)
    num_pixels = wide + tall + common.randint(-1, 1)
    pixels = common.sample(common.all_pixels(wide, tall), num_pixels)
    rows, cols = zip(*pixels)
    colors = common.random_colors(2)

  grid, output = common.grid(width, height), common.grid(wide, tall)
  for dr, dc in [(-1, -1), (-1, wide), (tall, -1), (tall, wide)]:
    grid[brow + dr][bcol + dc] = colors[1]
  for r, c in zip(rows, cols):
    grid[brow + r][bcol + c] = colors[0]
    output[r][c] = colors[1]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=7, height=7, rows=[0, 1, 1, 1, 2, 2],
               cols=[1, 0, 1, 2, 1, 2], wide=3, tall=3, brow=2, bcol=2,
               colors=[2, 4]),
      generate(width=9, height=12, rows=[0, 0, 1, 1, 1, 2, 2],
               cols=[1, 2, 1, 2, 4, 0, 3], wide=5, tall=3, brow=2, bcol=2,
               colors=[2, 3]),
      generate(width=14, height=12, rows=[0, 1, 2, 2, 2, 3, 3],
               cols=[1, 1, 0, 1, 2, 1, 2], wide=4, tall=4, brow=6, bcol=4,
               colors=[8, 6]),
      generate(width=18, height=12, rows=[0, 0, 1, 1, 2, 3, 3],
               cols=[3, 4, 2, 3, 6, 4, 6], wide=8, tall=4, brow=2, bcol=3,
               colors=[4, 8]),
  ]
  test = [
      generate(width=19, height=18,
               rows=[1, 1, 1, 2, 3, 4, 4, 4, 5, 5, 6, 7, 7],
               cols=[1, 6, 7, 1, 3, 3, 4, 5, 5, 8, 8, 4, 5], wide=10, tall=8,
               brow=3, bcol=3, colors=[3, 2]),
  ]
  return {"train": train, "test": test}

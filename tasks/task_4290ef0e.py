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


def generate(width=None, height=None, rows=None, cols=None, colors=None,
             lengths=None, b=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    lengths: a list of lengths of the borders
    b: the color of the background
  """
  if width is None:
    width, height = common.randint(13, 19), common.randint(13, 19)
    b = common.random_color()
    colors = common.random_colors(common.randint(4, 6), exclude=[b])
    lengths = []
    for i in range(len(colors)):
      min_length, max_length = min(i + 1, 2), i + (0 if i > 1 else 1)
      lengths.append(common.randint(min_length, max_length))
    # Keep drawing as long as (a) we overlap another pixel, or (b) we're unable
    # to draw in at least two separate quadrants.
    while True:
      grid = common.grid(width, height, b)
      rows = [common.randint(0, height - 1) for _ in range(len(colors))]
      cols = [common.randint(0, width - 1) for _ in range(len(colors))]
      illegal = False
      for idx, color in enumerate(colors):
        row, col, length, num_quad = rows[idx], cols[idx], lengths[idx], 0
        for r, c in [(-idx, -idx), (-idx, idx), (idx, -idx), (idx, idx)]:
          deltas, quad = [], 0
          for i in range(length):
            deltas += [(r, c + (i if c < 0 else -i))]
            deltas += [(r + (i if r < 0 else -i), c)]
          for dr, dc in deltas:
            pixel = common.get_pixel(grid, row + dr, col + dc)
            if pixel not in [-1, b, color]: illegal = True
            if pixel == b: quad = 1
            common.draw(grid, row + dr, col + dc, color)
          num_quad += quad
        if idx and num_quad < 2: illegal = True
      if not illegal: break

  grid = common.grid(width, height, b)
  output = common.grid(2 * len(colors) - 1, 2 * len(colors) - 1, b)
  for idx, color in enumerate(colors):
    row, col, length = rows[idx], cols[idx], lengths[idx]
    for r, c in [(-idx, -idx), (-idx, idx), (idx, -idx), (idx, idx)]:
      deltas = []
      for i in range(length):
        deltas += [(r, c + (i if c < 0 else -i))]
        deltas += [(r + (i if r < 0 else -i), c)]
      for dr, dc in deltas:
        common.draw(grid, row + dr, col + dc, color)
        output[len(colors) - 1 + dr][len(colors) - 1 + dc] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=17, height=13, rows=[0, 2, 4, 10], cols=[0, 13, 5, 13],
               colors=[4, 3, 1, 6], lengths=[1, 2, 2, 2], b=4),
      generate(width=18, height=18, rows=[6, 12, 14, 5], cols=[13, 2, 9, 5],
               colors=[0, 4, 2, 1], lengths=[1, 2, 2, 3], b=8),
      generate(width=18, height=18, rows=[16, 7, 4, 4, 6, 18],
               cols=[16, 8, 17, -1, 9, 8], colors=[6, 7, 8, 2, 1, 4],
               lengths=[1, 2, 2, 3, 3, 2], b=3),
  ]
  test = [
      generate(width=19, height=19, rows=[0, 4, 10, 16, 19, 1],
               cols=[0, 8, 5, 17, 8, 18], colors=[1, 8, 3, 6, 2, 4],
               lengths=[1, 2, 2, 2, 3, 5], b=1),
  ]
  return {"train": train, "test": test}

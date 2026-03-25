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


def generate(wide=None, tall=None, colors=None, row_buffer=None,
             col_buffer=None):
  """Returns input and output grids according to the given parameters.

  Args:
    wide: The width of the input grid.
    tall: The height of the input grid.
    colors: The colors of the output grid.
    row_buffer: The row buffer of the grid.
    col_buffer: The column buffer of the grid.
  """

  def draw():
    color_to_count = {color: colors.count(color) for color in colors}
    if len(set(color_to_count.keys())) != len(set(color_to_count.values())):
      return None, None
    count_to_color = {count: color for color, count in color_to_count.items()}
    counts = sorted(count_to_color.keys())
    mode = count_to_color[counts.pop()]  # Remove the most common color.
    inwidth, inheight = 5 * wide + col_buffer, 5 * tall + row_buffer
    outwidth, outheight = counts[-1], len(counts)
    grid = common.grid(inwidth, inheight)
    output = common.grid(outwidth, outheight)
    for row in range(4, inheight, 5):
      for col in range(inwidth):
        grid[row][col] = mode
    for col in range(4, inwidth, 5):
      for row in range(inheight):
        grid[row][col] = mode
    for i, color in enumerate(colors):
      r, c = i // wide, i % wide
      common.rect(grid, 2, 2, 5 * r + 1, 5 * c + 1, color)
    for r, count in enumerate(counts):
      color = count_to_color[count]
      for c in range(count):
        output[r][c] = color
    return grid, output

  if wide is None:
    wide, tall = common.randint(3, 4), common.randint(3, 4)
    row_buffer, col_buffer = common.randint(-2, 1), common.randint(-2, 1)
    subset = common.random_colors(wide + tall - 3)
    while True:
      colors = common.choices(subset, wide * tall)
      if len(set(colors)) != len(subset): continue
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(wide=3, tall=3, colors=[3, 1, 2, 2, 1, 3, 1, 3, 3], row_buffer=1,
               col_buffer=1),
      generate(wide=3, tall=4, colors=[4, 6, 8, 8, 6, 3, 6, 8, 4, 6, 6, 6],
               row_buffer=-1, col_buffer=-2),
      generate(wide=4, tall=3, colors=[4, 1, 1, 8, 2, 4, 2, 2, 4, 4, 2, 2],
               row_buffer=1, col_buffer=-2),
  ]
  test = [
      generate(wide=4, tall=4,
               colors=[4, 6, 3, 2, 6, 8, 8, 3, 8, 6, 2, 8, 2, 2, 8, 8],
               row_buffer=-1, col_buffer=1),
  ]
  return {"train": train, "test": test}

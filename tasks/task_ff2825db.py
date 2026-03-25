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


def generate(fgcolor=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    fgcolor: The foreground color.
    colors: A list of colors to use.
  """

  def draw():
    grid, output = common.grids(10, 10)
    common.hollow_rect(grid, 10, 9, 1, 0, fgcolor)
    for i in range(5):
      for j in range(2):
        output[0][2 * i + j] = grid[0][2 * i + j] = i + 1
    for row in range(7):
      for col in range(8):
        grid[row + 2][col + 1] = colors[row * 8 + col]
    subset = list(set(colors))
    if len(subset) != 3: return None, None
    subset.remove(0)
    counts = [colors.count(color) for color in subset]
    max_count = max(counts)
    mode = [color for color, count in zip(subset, counts) if count == max_count]
    if len(mode) != 1: return None, None
    common.hollow_rect(output, 10, 9, 1, 0, mode[0])
    min_row, max_row, min_col, max_col = None, None, None, None
    for row in range(7):
      for col in range(8):
        if grid[row + 2][col + 1] != mode[0]: continue
        if min_row is None:
          min_row, max_row, min_col, max_col = row, row, col, col
        min_row, max_row = min(min_row, row), max(max_row, row)
        min_col, max_col = min(min_col, col), max(max_col, col)
    wide, tall = max_col - min_col + 1, max_row - min_row + 1
    if wide < 2 or tall < 2: return None, None
    common.hollow_rect(output, wide, tall, 2 + min_row, 1 + min_col, mode[0])
    return grid, output

  if fgcolor is None:
    pair = common.sample([1, 2, 3, 4, 5], 3)
    fgcolor, color1, color2 = pair[0], pair[1], pair[2]
    freq1, freq2 = common.randint(1, 19), common.randint(1, 19)
    while True:
      colors = []
      wide, tall = common.randint(2, 8), common.randint(2, 7)
      brow, bcol = common.randint(0, 8 - wide), common.randint(0, 7 - tall)
      for row in range(7):
        for col in range(8):
          if row < brow or row >= brow + tall or col < bcol or col >= bcol + wide:
            colors.append(0)
            continue
          if common.randint(0, freq1) == 0:
            colors.append(color1)
          elif common.randint(0, freq2) == 0:
            colors.append(color2)
          else:
            colors.append(0)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(fgcolor=4, colors=[0, 0, 0, 0, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 5, 0,
                                  0, 0, 0, 5, 5, 0, 0, 0,
                                  0, 0, 0, 5, 1, 1, 0, 0,
                                  0, 5, 0, 5, 0, 0, 0, 0,
                                  0, 1, 0, 0, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0]),
      generate(fgcolor=2, colors=[0, 0, 3, 3, 3, 0, 0, 4,
                                  0, 3, 3, 0, 3, 3, 4, 3,
                                  0, 3, 0, 3, 0, 4, 3, 3,
                                  0, 3, 4, 0, 0, 0, 3, 4,
                                  0, 3, 0, 3, 3, 3, 4, 0,
                                  0, 3, 3, 3, 4, 3, 3, 3,
                                  0, 0, 0, 0, 0, 0, 0, 4]),
      generate(fgcolor=1, colors=[0, 0, 0, 0, 0, 0, 0, 2,
                                  0, 0, 2, 0, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 4, 0,
                                  4, 0, 0, 0, 4, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0,
                                  0, 0, 4, 0, 0, 4, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 2]),
  ]
  test = [
      generate(fgcolor=2, colors=[0, 0, 0, 0, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0,
                                  0, 0, 0, 1, 0, 0, 0, 0,
                                  0, 0, 0, 4, 0, 0, 0, 0,
                                  0, 0, 0, 0, 4, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0]),
      generate(fgcolor=5, colors=[0, 0, 0, 0, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 2, 0,
                                  0, 0, 1, 0, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 1, 0, 0,
                                  0, 0, 2, 0, 0, 2, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0]),
  ]
  return {"train": train, "test": test}

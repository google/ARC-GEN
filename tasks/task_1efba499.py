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


def generate(width=None, height=None, fgcolor=None, xpose=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    fgcolor: The foreground color of the grid.
    xpose: Whether to transpose the grid.
    colors: A list of colors to use.
  """

  if width is None:
    width = 12 if common.randint(0, 1) else 14
    height = 12 if common.randint(0, 1) else 14
    colors = common.shuffle(list(range(1, 10)))
    fgcolor = colors.pop()
    topcolors = [colors.pop()]
    if common.randint(0, 3) == 0: topcolors.append(colors.pop())
    botcolors = [colors.pop()]
    if common.randint(0, 3) == 0: botcolors.append(colors.pop())
    length = width if common.randint(0, 3) else (width - 1)
    start = common.randint(0, width - length)
    top = bot = mid = (height + common.randint(-1, 1)) // 2
    reset = common.randint(1, 5)
    grid = common.grid(width, height)
    for col in range(start, start + length):
      topcolor, botcolor = common.choice(topcolors), common.choice(botcolors)
      for row in range(min(top, bot), max(top, bot) + 1):
        grid[row][col] = fgcolor
      if common.randint(0, 9) == 0:  # Sometimes draw nothing.
        pass
      elif common.randint(0, 1) == 0:  # Sometimes draw one of each.
        row = common.randint(0, min(top, bot) - 1)
        grid[row][col] = topcolor
        row = common.randint(max(top, bot) + 1, height - 1)
        grid[row][col] = botcolor
      elif common.randint(0, 1) == 0:  # Sometimes draw top.
        for _ in range(1 if common.randint(0, 3) else 2):
          row = common.randint(0, min(top, bot) - 1)
          grid[row][col] = topcolor
      else:  # Sometimes draw bottom.
        for _ in range(1 if common.randint(0, 3) else 2):
          row = common.randint(max(top, bot) + 1, height - 1)
          grid[row][col] = botcolor
      reset -= 1
      if reset == 0:
        top, bot = top + common.randint(-1, 1), bot + common.randint(-1, 1)
        if top < mid - 1: top = mid - 1
        if top > mid + 1: top = mid + 1
        if bot > mid + 1: bot = mid + 1
        if bot < mid - 1: bot = mid - 1
        reset = common.randint(1, 5)
    xpose = common.randint(0, 1)
    if xpose:
      grid = common.transpose(grid)
      width, height = height, width
    colors = common.flatten(grid)

  grid, output = common.grids(width, height)
  for i, color in enumerate(colors):
    grid[i // width][i % width] = color
    output[i // width][i % width] = color if color == fgcolor else 0
  if xpose:
    grid, output = common.transpose(grid), common.transpose(output)
    width, height = height, width
  for col in range(width):
    strip = [grid[row][col] for row in range(height) if grid[row][col]]
    strip = common.remove_duplicates(strip)
    if len(strip) < 3:  # If less than 3 colors, keep the column as is.
      for row in range(height):
        output[row][col] = grid[row][col]
      continue
    for row in range(1, height - 1):
      if output[row][col] == 0 and output[row + 1][col] == fgcolor:
        output[row][col] = strip[2]
      if output[row - 1][col] == fgcolor and output[row][col] == 0:
        output[row][col] = strip[0]
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=12, height=12, fgcolor=8, xpose=0,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       4, 4, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 0, 0,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0,
                       0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 6, 0, 0, 0, 6, 0, 6,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(width=12, height=12, fgcolor=3, xpose=0,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 7, 0, 0, 0, 7, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0,
                       0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0,
                       0, 3, 3, 0, 0, 0, 0, 0, 0, 3, 3, 0,
                       3, 0, 0, 3, 3, 0, 3, 3, 3, 3, 3, 0,
                       0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 2, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0,
                       2, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(width=14, height=12, fgcolor=3, xpose=1,
               colors=[0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 9, 0, 0, 0, 3, 0, 0, 0, 5, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 9, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0,
                       0, 0, 9, 0, 0, 3, 3, 3, 0, 0, 5, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 9, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0,
                       0, 0, 9, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0,
                       0, 0, 9, 0, 0, 0, 3, 0, 0, 0, 5, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 9, 0, 0, 0, 3, 0, 0, 0, 5, 0, 0, 0]),
  ]
  test = [
      generate(width=14, height=12, fgcolor=4, xpose=1,
               colors=[0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 1, 0, 0, 4, 4, 0, 0, 0, 6, 0, 0, 0,
                       0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 1, 0, 0, 4, 4, 4, 0, 0, 0, 3, 0, 0,
                       0, 0, 1, 0, 0, 4, 4, 4, 0, 3, 0, 0, 0, 0,
                       0, 0, 1, 0, 0, 4, 4, 4, 0, 0, 6, 0, 0, 0,
                       0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0,
                       0, 0, 1, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0,
                       0, 1, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0,
                       0, 1, 0, 0, 0, 0, 4, 0, 0, 0, 6, 0, 0, 0,
                       0, 0, 0, 1, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 1, 0, 0, 4, 0, 0, 0, 6, 0, 0, 0]),
  ]
  return {"train": train, "test": test}

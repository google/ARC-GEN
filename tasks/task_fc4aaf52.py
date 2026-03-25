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


def generate(bgcolor=None, fgcolor=None, rows=None, cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    bgcolor: The background color.
    fgcolor: The foreground color.
    rows: The rows of the pixels.
    cols: The columns of the pixels.
  """

  def draw():
    grid, output = common.grids(16, 16, 8)
    for row, col in zip(rows, cols):
      grid[7 - row][col] = grid[8 + row][col] = bgcolor
    for row in range(1, 15):
      for col in range(1, 15):
        cyans = 0
        for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
          if grid[row + dr][col + dc] == 8: cyans += 1
        if not cyans: grid[row][col] = fgcolor
    # First, invert the image.
    for row in range(16):
      for col in range(16):
        if grid[row][col] == bgcolor: output[row][col] = fgcolor
        if grid[row][col] == fgcolor: output[row][col] = bgcolor
    # Second, shift the top until we're done.
    while True:
      done = True
      for col in range(16):
        if output[7][col] != 8 and output[8][col] != 8: done = False
      if done: break
      for col in range(15, 0, -1):
        for row in range(8):
          output[row][col] = output[row][col - 1]
    if len(set(common.flatten(grid))) != 3: return None, None
    return grid, output

  if bgcolor is None:
    colors = common.sample([0, 1, 2, 3, 4, 5, 6, 7, 9], 2)
    bgcolor, fgcolor = colors[0], colors[1]
    while True:
      length = common.randint(3, 7)
      start = common.randint(1, 8 - length)
      rows, cols = [], []
      for row in range(5):
        for col in range(start, start + length):
          rows.append(row)
          cols.append(col)
        length += common.randint(-2, 2)
        if length < 1: break
        if length > 7: length = 7
        start += common.randint(-1, 1)
        if start < 1: start = 1
        if start + length > 8: start = 8 - length
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(bgcolor=0, fgcolor=5, rows=[0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 3],
               cols=[3, 4, 5, 2, 3, 4, 5, 6, 3, 4, 5, 4]),
      generate(bgcolor=1, fgcolor=2, rows=[0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3],
               cols=[1, 2, 3, 4, 5, 1, 2, 3, 1, 2, 3, 2]),
  ]
  test = [
      generate(bgcolor=4, fgcolor=9,
               rows=[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2],
               cols=[1, 2, 3, 4, 5, 6, 7, 2, 3, 4, 5, 6, 3, 4, 5]),
  ]
  return {"train": train, "test": test}

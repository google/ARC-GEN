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


def generate(rows=None, cols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: The rows of the shapes.
    cols: The columns of the shapes.
    colors: The colors of the shapes.
  """

  def draw():
    index = -1
    bad = False
    grid, output = common.grids(9, 9, 7)
    hidden = common.grid(9, 9, -1)
    def put(r, c, color):
      nonlocal index, bad, grid, output, hidden
      if grid[r][c] != 7: bad = True
      grid[r][c] = 6
      output[r][c] = color
      hidden[r][c] = index
    for row, col, color in zip(rows, cols, colors):
      index += 1
      if color == 2:
        put(row, col, 2)
        put(row + 1, col, 2)
        put(row + 2, col, 2)
      if color == 3:
        put(row, col + 1, 3)
        put(row + 1, col, 3)
        put(row + 1, col + 1, 3)
        put(row + 1, col + 2, 3)
        put(row + 2, col + 1, 3)
      if color == 4:
        put(row, col, 4)
        put(row, col + 1, 4)
        put(row + 1, col + 1, 4)
      if color == 5:
        put(row, col, 5)
        put(row, col + 1, 5)
        put(row, col + 2, 5)
        put(row + 1, col, 5)
        put(row + 1, col + 1, 5)
        put(row + 1, col + 2, 5)
      if color == 8:
        put(row, col, 8)
        put(row, col + 1, 8)
        put(row + 1, col + 1, 8)
        put(row + 1, col + 2, 8)
      if color == 9:
        put(row, col, 9)
        put(row + 1, col, 9)
    # Check that no two colors share an adjacent edge.
    for r in range(9):
      for c in range(8):
        if hidden[r][c] == -1 or hidden[r][c + 1] == -1: continue
        if hidden[r][c] != hidden[r][c + 1]: bad = True
    for r in range(8):
      for c in range(9):
        if hidden[r][c] == -1 or hidden[r + 1][c] == -1: continue
        if hidden[r][c] != hidden[r + 1][c]: bad = True
    if bad: return None, None
    return grid, output

  if rows is None:
    extra = common.randint(0, 2)
    while True:
      wides = [0, 0, 1, 3, 2, 3, 0, 0, 3, 1]
      talls = [0, 0, 3, 3, 2, 2, 0, 0, 2, 2]
      colors = [2, 3, 4, 5, 8, 9]
      colors += common.sample(colors, extra)
      colors = common.shuffle(colors)
      wides = [wides[color] for color in colors]
      talls = [talls[color] for color in colors]
      rows = [common.randint(0, 9 - tall) for tall in talls]
      cols = [common.randint(0, 9 - wide) for wide in wides]
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 2, 2, 3, 4, 6, 7], cols=[0, 4, 2, 8, 6, 1, 7, 4],
               colors=[4, 8, 3, 2, 9, 2, 4, 5]),
      generate(rows=[1, 1, 2, 5, 6, 7], cols=[0, 4, 6, 4, 8, 1],
               colors=[3, 9, 4, 8, 2, 5]),
  ]
  test = [
      generate(rows=[0, 0, 2, 3, 6, 6, 7], cols=[0, 4, 8, 3, 0, 7, 5],
               colors=[3, 8, 2, 5, 4, 4, 9]),
  ]
  return {"train": train, "test": test}

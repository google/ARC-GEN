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


def generate(width=None, height=None, rows=None, cols=None, lines=None,
             xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    lines: the horizontal lines
    xpose: whether to transpose the grids
  """

  def draw(grid, output):
    for line in lines:
      for c in range(width):
        output[line][c] = grid[line][c] = common.cyan()
    for row, col in zip(rows, cols):
      grid[row][col] = common.red()
      for line in lines:
        r, dr = row, -1 if line < row else 1
        while r != line:
          if output[r][col] == common.cyan(): break
          output[r][col], r = common.red(), r + dr
        if r == line:
          for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
              output[r + dr][col + dc] = common.cyan()
          output[r][col] = common.red()
    return grid != output

  if width is None:
    while True:
      width, height = common.randint(12, 20), common.randint(12, 20)
      num_lines = common.randint(1, 2)
      if num_lines == 1:
        lines = [height // 2]
      else:
        lines = [common.randint(height // 5, 2 * height // 5),
                 common.randint(3 * height // 5, 4 * height // 5)]
      rows, cols = [], []
      for c in range(1, width - 1):
        r = common.randint(0, height - 1)
        if r in lines or r - 1 in lines or r + 1 in lines: continue
        if cols and cols[-1] + 4 > c:   # Need to ensure spacing between boxes.
          if num_lines == 1: continue
          if min(r, rows[-1]) > lines[0] or max(r, rows[-1]) < lines[1]: continue
        if common.randint(0, 2): continue
        rows.append(r)
        cols.append(c)
      grid, output = common.grids(width, height)
      if draw(grid, output): break

  grid, output = common.grids(width, height)
  draw(grid, output)
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=13, height=13, rows=[2, 10], cols=[2, 8], lines=[6],
               xpose=0),
      generate(width=13, height=18, rows=[8], cols=[4], lines=[3, 14], xpose=1),
      generate(width=12, height=17, rows=[2, 10], cols=[8, 4], lines=[7, 13],
               xpose=0),
  ]
  test = [
      generate(width=17, height=19, rows=[1, 8, 15, 16], cols=[2, 8, 1, 14],
               lines=[4, 12], xpose=1),
  ]
  return {"train": train, "test": test}

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

  def draw():
    if common.overlaps_1d(lines, [4] * len(lines)): return None, None
    if common.overlaps_1d(cols, [4] * len(cols)): return None, None
    grid, output = common.grids(width, height)
    for line in lines:
      for c in range(width):
        output[line][c] = grid[line][c] = common.red()
    for row, col in zip(rows, cols):
      common.hollow_rect(grid, 3, 3, row - 1, col - 1, 3)
      for line in lines:
        color = 3 if line == row else 1
        common.hollow_rect(output, 3, 3, line - 1, col - 1, color)
      for r in range(height):
        if output[r][col] == 0: output[r][col] = 1
    if xpose: grid, output = common.transpose(grid), common.transpose(output)
    return grid, output

  if width is None:
    num_lines = common.randint(1, 4)
    num_boxes = common.randint(1, num_lines)
    while True:
      width, height = common.randint(12, 20), common.randint(12, 20)
      lines = [common.randint(1, height - 2) for _ in range(num_lines)]
      cols = [common.randint(1, width - 2) for _ in range(num_boxes)]
      rows = common.sample(lines, num_boxes)
      xpose = common.randint(0, 1)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=12, height=12, rows=[4], cols=[6], lines=[4],
               xpose=1),
      generate(width=15, height=12, rows=[3, 9], cols=[2, 11], lines=[3, 9],
               xpose=1),
      generate(width=14, height=16, rows=[3, 14], cols=[4, 10],
               lines=[3, 8, 14], xpose=0),
      generate(width=10, height=10, rows=[1], cols=[5], lines=[1, 6], xpose=0),
  ]
  test = [
      generate(width=16, height=18, rows=[2, 11], cols=[2, 12],
               lines=[2, 7, 11, 16], xpose=1),
  ]
  return {"train": train, "test": test}

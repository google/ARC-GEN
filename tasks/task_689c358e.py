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


def generate(rows=None, cols=None, angles=None, colors=[2, 5, 8, 9]):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: The rows of the crosses.
    cols: The columns of the crosses.
    angles: The angles of the crosses.
    colors: The colors of the crosses.
  """

  def draw():
    grid, output = common.grids(11, 11, 7)
    def put(g, r, c, color):
      if g[r][c] != 7: return False
      g[r][c] = color
      return True
    common.hollow_rect(grid, 11, 11, 0, 0, 6)
    common.hollow_rect(output, 11, 11, 0, 0, 6)
    for row, col, angle, color in zip(rows, cols, angles, colors):
      for dr, dc in [(0, -1), (-1, 0), (0, 0), (1, 0), (0, 1)]:
        if not put(grid, row + dr, col + dc, color): return None, None
        if not put(output, row + dr, col + dc, color): return None, None
      r, c = row, col
      if angle == 0:
        r, c, output[10][col], output[0][col] = row - 2, col, color, 0
      if angle == 1:
        r, c, output[row][0], output[row][10] = row, col + 2, color, 0
      if angle == 2:
        r, c, output[0][col], output[10][col] = row + 2, col, color, 0
      if angle == 3:
        r, c, output[row][10], output[row][0] = row, col - 2, color, 0
      if not put(grid, r, c, color): return None, None
      if not put(output, r, c, color): return None, None
    return grid, output

  if rows is None:
    while True:
      rows, cols, angles = [], [], []
      for _ in range(4):
        angle, lb_row, lb_col, ub_row, ub_col = common.randint(0, 3), 2, 2, 8, 8
        if angle == 0: lb_row, ub_row = 4, 7
        if angle == 1: lb_col, ub_col = 3, 6
        if angle == 2: lb_row, ub_row = 3, 6
        if angle == 3: lb_col, ub_col = 4, 7
        angles.append(angle)
        rows.append(common.randint(lb_row, ub_row))
        cols.append(common.randint(lb_col, ub_col))
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[7, 8, 3, 5], cols=[7, 3, 8, 3], angles=[3, 1, 2, 1]),
      generate(rows=[7, 3, 3, 8], cols=[7, 8, 4, 3], angles=[3, 2, 2, 1]),
  ]
  test = [
      generate(rows=[4, 3, 8, 7], cols=[6, 2, 4, 8], angles=[2, 2, 1, 0]),
  ]
  return {"train": train, "test": test}

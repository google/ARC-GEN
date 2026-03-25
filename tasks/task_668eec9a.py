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


def generate(rows=None, cols=None, angles=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: The rows of the lines.
    cols: The columns of the lines.
    angles: The angles of the lines.
    colors: The colors of the lines.
  """

  def draw():
    grid, output = common.grid(16, 16, 7), common.grid(3, 5, 7)
    for i, (row, col, angle, color) in enumerate(zip(rows, cols, angles, colors)):
      r, c, is_horiz = row, col, row == 15
      while r < 16:
        # First, check that there are no other lines below.
        if not is_horiz:
          for rr in range(r, 16):
            if grid[rr][c] != 7: return None, None
        # Second, draw the next pixel, and adjust its position.
        common.draw(grid, r, c, color)
        r, c = (r + 1) if not is_horiz else r, c + angle
        if c < 0 or c >= 16: break
        if is_horiz and (c < 1 or c >= 15): break
      for c in range(0, 3):
        output[i + 5 - len(rows)][c] = color
    return grid, output

  if rows is None:
    num_diags = common.randint(3, 4)
    extra_line = common.randint(0, 1)
    while True:
      rows = sorted(common.sample(list(range(1, 13)), num_diags))
      cols = [common.randint(3, 13) for _ in range(num_diags)]
      angles = [2 * common.randint(0, 1) - 1 for _ in range(num_diags)]
      if extra_line:
        rows.append(15)
        cols.append(common.randint(6, 10))
        angles.append(2 * common.randint(0, 1) - 1)
      colors = common.sample([1, 2, 3, 4, 5, 6, 8, 9], len(rows))
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[5, 10, 12, 15], cols=[5, 6, 6, 10], angles=[1, 1, -1, -1],
               colors=[3, 9, 1, 4]),
      generate(rows=[3, 8, 11], cols=[6, 8, 7], angles=[1, -1, 1],
               colors=[1, 8, 2]),
      generate(rows=[2, 8, 11, 12, 15], cols=[3, 5, 6, 6, 15],
               angles=[1, 1, -1, 1, -1], colors=[4, 9, 1, 3, 8]),
  ]
  test = [
      generate(rows=[6, 10, 11, 15], cols=[10, 8, 6, 3], angles=[-1, 1, 1, 1],
               colors=[5, 1, 4, 3]),
  ]
  return {"train": train, "test": test}

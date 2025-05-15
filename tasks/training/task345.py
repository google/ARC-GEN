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


def generate(rows=None, cols=None, starts=None, size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    starts: a list of vertical coordinates where the lines start
    size: the width and height of the (square) grid
  """

  def draw(grid, output):
    legal = False
    for r, c in zip(rows, cols):
      output[r][c] = grid[r][c] = common.gray()
    for start in starts:
      r, c = size - 1, start
      output[r][c] = grid[r][c] = common.red()
      while r > 0:
        if output[r - 1][c] == common.gray():
          c += 1
          legal = True
        else:
          r -= 1
        output[r][c] = common.red()
    return legal

  if rows is None:
    while True:
      rows, cols, starts, start = [], [], [], 1
      while start + 1 < size:
        starts.append(start)
        if not common.randint(0, 3):  # Sometimes, we don't add a gray dot.
          start += 2
        else:
          rows.append(common.randint(2, 6))
          cols.append(start + common.randint(-1, 1))
          start += common.randint(3, 4)
      grid, output = common.grids(size, size)
      if draw(grid, output): break

  grid, output = common.grids(size, size)
  draw(grid, output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[3, 5], cols=[6, 2], starts=[1, 4, 6]),
      generate(rows=[3, 5, 6], cols=[5, 1, 8], starts=[1, 4, 7]),
  ]
  test = [
      generate(rows=[2, 4, 6], cols=[7, 1, 4], starts=[1, 4, 8]),
  ]
  return {"train": train, "test": test}

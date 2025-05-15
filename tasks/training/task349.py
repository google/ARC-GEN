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


def generate(size=None, rows=None, cols=None, radii=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    radii: a list of radius values
  """
  if size is None:
    factor = common.randint(2, 6)
    tuples, size = [], 5 * factor
    for _ in range(factor):
      radius = common.randint(1, factor - 1)
      row = common.randint(1, size)
      col = common.randint(0, size - 2 * radius)
      overlaps = False
      for r, c, i in tuples:
        if col + 3 * radius < c - i or c + 3 * i < col - radius: continue
        if row - 3 * radius > r + i or r - 3 * i > row + radius: continue
        overlaps = True
      if overlaps: continue
      tuples.append((row, col, radius))
    # We need to sort all the death stars by row.
    tuples.sort(key=lambda x: x[0])
    rows, cols, radii = zip(*tuples)

  grid, output = common.grids(size, size)
  for r, c, radius in zip(rows, cols, radii):
    # Draw the blue beams.
    for row in range(r + 1, size):
      for dc in range(2 * radius):
        common.draw(output, row, c + dc, common.blue())
    # Draw the green halos.
    for dr in range(4 * radius):
      for dc in range(4 * radius):
        common.draw(output, r - dr + radius, c + dc - radius, common.green())
    # Draw the maroon centers.
    for dr in range(2 * radius):
      for dc in range(2 * radius):
        common.draw(grid, r - dr, c + dc, common.maroon())
        common.draw(output, r - dr, c + dc, common.maroon())
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=10, rows=[1, 8], cols=[6, 1], radii=[1, 1]),
      generate(size=15, rows=[5, 7, 10], cols=[8, 3, 13], radii=[2, 1, 1]),
      generate(size=20, rows=[4, 9, 17], cols=[2, 15, 6], radii=[1, 2, 3]),
      generate(size=20, rows=[1, 11, 14], cols=[7, 2, 14], radii=[2, 2, 3]),
  ]
  test = [
      generate(size=30, rows=[5, 10, 21, 23], cols=[16, 9, 21, 4],
               radii=[2, 2, 3, 1]),
  ]
  return {"train": train, "test": test}

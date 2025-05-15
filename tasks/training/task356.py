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


def generate(rows=None, cols=None, size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    size: the size of the grid
  """
  if rows is None:
    while True:
      pixels = common.random_pixels(size, size, 0.05)
      if pixels: break
    rows, cols = zip(*pixels)

  grid, output = common.grids(size, size)
  for r, c in zip(rows, cols):
    output[r][c] = grid[r][c] = common.cyan()
  for r1, c1 in zip(rows, cols):
    for r2, c2 in zip(rows, cols):
      if r1 == r2:
        for c in range(min(c1, c2), max(c1, c2)):
          output[r1][c] = common.cyan()
      if c1 == c2:
        for r in range(min(r1, r2), max(r1, r2)):
          output[r][c1] = common.cyan()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[3, 3, 7, 9], cols=[1, 6, 4, 6]),
      generate(rows=[1, 3, 6, 6, 8], cols=[7, 2, 5, 9, 2]),
      generate(rows=[1, 1, 4, 7, 7, 9], cols=[1, 5, 1, 5, 9, 2]),
  ]
  test = [
      generate(rows=[1, 2, 3, 5, 8, 8], cols=[1, 3, 7, 1, 4, 7]),
  ]
  return {"train": train, "test": test}

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


def generate(rows=None, cols=None, size=3):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    size: the width and height of the (square) grid
  """
  if rows is None:
    while True:  # Avoid ambiguous cases (e.g., symmetrically horiz only)
      pixels = common.all_pixels(size, size)
      pixels = common.sample(pixels, common.randint(1, 4))
      rows, cols = zip(*pixels)
      grid, force_symmetric = common.grid(size, size), common.randint(0, 1)
      for r, c in zip(rows, cols):
        grid[r][c] = common.red()
        if not force_symmetric: continue
        grid[r][size - c - 1] = grid[size - r - 1][c] = common.red()
        grid[size - r - 1][size - c - 1] = common.red()
      horiz, vert = True, True
      for r in range(size):
        for c in range(size):
          horiz = horiz and grid[r][c] == grid[r][size - c - 1]
          vert = vert and grid[r][c] == grid[size - r - 1][c]
      if horiz != vert: continue
      # Convert the grid (possibly now symmetric) back into rows & cols
      rows, cols = [], []
      for r in range(size):
        for c in range(size):
          if not grid[r][c]:
            continue
          rows.append(r)
          cols.append(c)
      break

  grid, output = common.grid(size, size), common.grid(1, 1)
  for r, c in zip(rows, cols):
    grid[r][c] = common.red()
  symmetric = True
  for r in range(size):
    for c in range(size):
      symmetric = symmetric and grid[r][c] == grid[r][size - c - 1]
  output[0][0] = common.blue() if symmetric else common.orange()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 2, 2], cols=[0, 2, 1, 0, 2]),
      generate(rows=[0, 1, 2], cols=[0, 0, 1]),
      generate(rows=[0, 0, 1, 1, 2, 2], cols=[0, 2, 0, 2, 0, 2]),
      generate(rows=[1, 1], cols=[0, 2]),
      generate(rows=[0, 0, 1, 1], cols=[0, 1, 1, 2]),
      generate(rows=[0, 0, 1], cols=[0, 1, 1]),
  ]
  test = [
      generate(rows=[0, 0, 1, 1, 1, 2, 2], cols=[0, 2, 0, 1, 2, 0, 2]),
      generate(rows=[1, 2], cols=[0, 0]),
  ]
  return {"train": train, "test": test}

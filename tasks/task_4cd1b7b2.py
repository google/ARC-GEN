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


def generate(colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: colors of the pixels.
  """

  def solve(ingrid):
    grid = [list(row) for row in ingrid]
    changed = True
    while changed:
      changed = False
      for r in range(4):
        values = [grid[r][c] for c in range(4) if grid[r][c] != 0]
        if len(values) != 3: continue
        value = 10 - sum(values)
        for c in range(4):
          if grid[r][c] == 0: grid[r][c] = value
        changed = True
      for c in range(4):
        values = [grid[r][c] for r in range(4) if grid[r][c] != 0]
        if len(values) != 3: continue
        value = 10 - sum(values)
        for r in range(4):
          if grid[r][c] == 0: grid[r][c] = value
        changed = True
    return grid

  def create_grid():
    rows = []
    for _ in range(4):
      while True:
        candidate = common.shuffle([1, 2, 3, 4])
        good = True
        for row in rows:
          for c in range(4):
            if row[c] == candidate[c]: good = False
        if good: break
      rows.append(candidate)
    return rows

  def strip_grid(grid):
    num_zeroed = 0
    strips = common.shuffle([(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3)])
    for strip in strips:
      cdir, val = strip
      if cdir == 1 and sum([grid[val][r] for r in range(4)]) == 10:
        grid[val][common.randint(0, 3)] = 0
        num_zeroed += 1
      if cdir == 0 and sum([grid[c][val] for c in range(4)]) == 10:
        grid[common.randint(0, 3)][val] = 0
        num_zeroed += 1
    return num_zeroed

  if colors is None:
    num_zeroes = common.randint(5, 6)
    while True:
      grid = create_grid()
      if strip_grid(grid) == num_zeroes: break
    colors = []
    for row in grid:
      colors.extend(row)

  grid = common.grid(4, 4)
  for i, color in enumerate(colors):
    grid[i // 4][i % 4] = color
  output = solve(grid)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[0, 4, 2, 3, 4, 1, 0, 2, 0, 3, 4, 0, 3, 0, 1, 4]),
      generate(colors=[1, 0, 3, 4, 0, 0, 2, 1, 2, 1, 4, 0, 0, 3, 1, 2]),
      generate(colors=[3, 0, 2, 1, 1, 0, 0, 0, 4, 3, 0, 2, 0, 1, 4, 3]),
  ]
  test = [
      generate(colors=[0, 1, 2, 3, 0, 3, 1, 0, 3, 0, 4, 1, 0, 4, 0, 2]),
  ]
  return {"train": train, "test": test}

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


def generate(width=None, height=None, rows=None, cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    rows: The rows of the boxes.
    cols: The columns of the boxes.
  """

  def draw():
    grid, output = common.grids(width, height)
    # First, compute the orange path.
    path, angles = [0], [30]
    while True:
      best_dist, best_nodes, best_angles = 30, [], []
      for i, (row, col) in enumerate(zip(rows, cols)):
        if i in path: continue
        if row == rows[path[-1]]:
          dist = abs(col - cols[path[-1]])
          angle = 1 if col < cols[path[-1]] else 3
        elif col == cols[path[-1]]:
          dist = abs(row - rows[path[-1]])
          angle = 0 if col < cols[path[-1]] else 2
        else: continue
        if abs(angle - angles[-1]) == 2: continue  # Prevent "doubling back"
        if best_dist > dist: best_dist, best_nodes, best_angles = dist, [], []
        if best_dist == dist: best_nodes, best_angles = best_nodes + [i], best_angles + [angle]
      if not best_nodes: break
      if len(best_nodes) > 1: return None, None  # Ill-defined case.
      path.append(best_nodes[0])
      angles.append(best_angles[0])
    # Second, draw the orange path.
    for i in range(1, len(path)):
      prev, curr = path[i - 1], path[i]
      min_row, max_row = min(rows[prev], rows[curr]), max(rows[prev], rows[curr])
      min_col, max_col = min(cols[prev], cols[curr]), max(cols[prev], cols[curr])
      if rows[prev] == rows[curr]:
        max_row, min_col, max_col = max_row + 1, min_col + 2, max_col - 1
      if cols[prev] == cols[curr]:
        max_col, min_row, max_row = max_col + 1, min_row + 2, max_row - 1
      for row in range(min_row, max_row + 1):
        for col in range(min_col, max_col + 1):
          if output[row][col] != 0: return None, None  # Ill-defined case.
          output[row][col] = 7
    # Third, draw the original boxes.
    for i, (row, col) in enumerate(zip(rows, cols)):
      for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        r, c = row + dr, col + dc
        if output[r][c] != 0: return None, None  # Ill-defined case.
        output[r][c] = grid[r][c] = 8 if i else 2
    return grid, output

  if width is None:
    width, height = common.randint(15, 30), common.randint(15, 30)
    path_length = (width + height) // 6 + 1
    while True:
      row, col = common.randint(1, height - 3), common.randint(1, width - 3)
      rows, cols = [], []
      good = True
      # First, attempt to create a wandering path.
      for _ in range(path_length):
        rows, cols = rows + [row], cols + [col]
        if common.randint(0, 1): row += common.randint(0, width) - width // 2
        else: col += common.randint(0, height) - height // 2
        if row < 1 or col < 1 or row + 3 > height or col + 3 > width:
          good = False
      if not good: continue  # Try again if some points are out of bounds.
      # Second, add a few random points.
      for _ in range(common.randint(0, path_length // 2)):
        rows.append(common.randint(1, height - 3))
        cols.append(common.randint(1, width - 3))
      if common.overlaps(rows, cols, [3] * len(cols), [3] * len(rows), 0):
        continue
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=18, height=16, rows=[6, 6, 6], cols=[8, 1, 13]),
      generate(width=28, height=26,
               rows=[21, 1, 6, 6, 11, 11, 11, 15, 16, 21, 21, 21],
               cols=[2, 1, 3, 14, 3, 7, 14, 24, 7, 7, 14, 21]),
      generate(width=25, height=26,
               rows=[1, 1, 4, 4, 10, 10, 14, 14, 17, 20, 20],
               cols=[3, 10, 5, 19, 3, 10, 10, 15, 21, 3, 15]),
      generate(width=18, height=26, rows=[23, 1, 6, 6, 17, 17],
               cols=[5, 5, 5, 11, 5, 11]),
  ]
  test = [
      generate(width=23, height=22,
               rows=[3, 3, 3, 6, 8, 8, 12, 14, 14, 16, 19, 19],
               cols=[4, 11, 19, 1, 7, 11, 15, 4, 7, 19, 4, 13]),
  ]
  return {"train": train, "test": test}

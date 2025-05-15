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


def generate(width=None, height=None, rows=None, cols=None, boxrows=None,
             boxcols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the (square) grid
    height: the height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    boxrows: a list of vertical coordinates where boxes should be placed
    boxcols: a list of horizontal coordinates where boxes should be placed
  """

  def maybe_add(queue, visited, r, c):
    if r < 0 or r >= height or c < 0 or c >= width: return False
    if not grid[r][c] or (r, c) in queue or (r, c) in visited: return False
    queue.append((r, c))
    return grid[r][c] == common.red()

  def path_exists(diags_allowed=False):
    neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    if diags_allowed:
      neighbors.extend([(-1, -1), (1, -1), (-1, 1), (1, 1)])
    queue = [(boxrows[0], boxcols[0]), (boxrows[0], boxcols[0] + 1),
             (boxrows[0] + 1, boxcols[0]), (boxrows[0] + 1, boxcols[0] + 1)]
    visited, exists = [], False
    while queue:
      r, c = queue.pop()
      visited.append((r, c))
      for dr, dc in neighbors:
        exists = exists or maybe_add(queue, visited, r + dr, c + dc)
    return exists

  if width is None:
    width, height = common.randint(5, 8), common.randint(5, 8)
    pixels = common.random_pixels(width, height, 0.4)
    rows, cols = zip(*pixels)
    num_boxes = 2
    while True:
      boxrows = [common.randint(0, height - 2) for _ in range(num_boxes)]
      boxcols = [common.randint(0, width - 2) for _ in range(num_boxes)]
      lengths = [2] * num_boxes
      if common.overlaps(boxrows, boxcols, lengths, lengths, 1): continue
      grid = common.grid(width, height)
      for r, c in zip(rows, cols):
        grid[r][c] = common.cyan()
      for r, c in zip(boxrows, boxcols):
        grid[r][c] = grid[r][c + 1] = common.red()
        grid[r + 1][c] = grid[r + 1][c + 1] = common.red()
      if path_exists() == path_exists(True): break  # prevent ambiguous cases

  grid, output = common.grid(width, height), common.grid(1, 1)
  for r, c in zip(rows, cols):
    grid[r][c] = common.cyan()
  for r, c in zip(boxrows, boxcols):
    grid[r][c] = grid[r][c + 1] = common.red()
    grid[r + 1][c] = grid[r + 1][c + 1] = common.red()
  output[0][0] = common.cyan() if path_exists() else common.black()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=5, height=5, rows=[0, 0, 1, 2, 4, 4],
               cols=[2, 4, 2, 4, 0, 1], boxrows=[1, 3], boxcols=[0, 3]),
      generate(width=7, height=5, rows=[0, 1, 1, 1, 2, 2, 3, 4, 4],
               cols=[1, 3, 4, 5, 2, 3, 2, 1, 4], boxrows=[1, 2],
               boxcols=[0, 5]),
      generate(width=7, height=6,
               rows=[0, 0, 0, 1, 2, 2, 2, 3, 3, 4, 4, 4, 4, 5],
               cols=[0, 3, 4, 6, 1, 2, 5, 2, 6, 0, 2, 3, 4, 0], boxrows=[0, 4],
               boxcols=[1, 5]),
      generate(width=7, height=6, rows=[0, 0, 1, 1, 1, 2, 2, 3, 4, 4, 5, 5, 5],
               cols=[0, 1, 1, 2, 6, 3, 5, 0, 4, 6, 3, 4, 6], boxrows=[0, 4],
               boxcols=[4, 1]),
      generate(width=7, height=6, rows=[0, 0, 1, 2, 3, 3, 4, 4, 5, 5],
               cols=[0, 5, 5, 0, 2, 5, 2, 6, 0, 5], boxrows=[1, 4],
               boxcols=[2, 3]),
      generate(width=6, height=6, rows=[0, 0, 1, 1, 2, 3, 3, 4, 5, 5, 5],
               cols=[0, 5, 0, 2, 4, 2, 4, 5, 1, 2, 4], boxrows=[0, 3],
               boxcols=[3, 0]),
  ]
  test = [
      generate(width=6, height=8,
               rows=[0, 0, 0, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 6, 7, 7],
               cols=[2, 3, 5, 3, 0, 1, 5, 1, 2, 3, 0, 2, 5, 2, 0, 1, 5],
               boxrows=[0, 5], boxcols=[0, 3]),
      generate(width=6, height=8,
               rows=[0, 1, 2, 2, 2, 3, 3, 4, 5, 5, 7, 7, 7],
               cols=[1, 3, 1, 2, 3, 1, 5, 3, 0, 5, 1, 3, 4],
               boxrows=[1, 5], boxcols=[4, 1]),
  ]
  return {"train": train, "test": test}

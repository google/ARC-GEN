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


def generate(height=None, rows=None, cols=None, color=None, width=12):
  """Returns input and output grids according to the given parameters.

  Args:
    height: the height of the grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    color: a digit representing a color to be used
    width: the width of the grid
  """
  if height is None:
    height = common.randint(10, 12)
    row = common.randint(height // 3, 2 * height // 3)
    col = common.randint(width // 3, 2 * width // 3)
    num_pixels = common.randint(8, 12)
    pixels, queue = [], [(row, col)]
    def neighbor_count(r, c):
      count = 0
      for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        count += 1 if (r + dr, c + dc) in pixels else 0
      return count
    while queue:
      queue_idx = common.randint(0, len(queue) - 1)
      r, c = queue.pop(queue_idx)
      if r == 0 or r == height - 1 or c == 0 or c == width - 1: continue
      if neighbor_count(r, c) > 1 or (r, c) in pixels: continue
      pixels.append((r, c))
      if len(pixels) == num_pixels: break
      for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        queue.append((r + dr, c + dc))
    rows, cols = zip(*pixels)
    color = common.random_color()

  min_row, max_row = min(rows), max(rows)
  min_col, max_col = min(cols), max(cols)
  grid = common.grid(width, height)
  output = common.grid(max_col - min_col + 1, max_row - min_row + 1)
  for r, c in zip(rows, cols):
    output[r - min_row][c - min_col] = grid[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(height=10, rows=[2, 2, 2, 3, 4, 4, 4, 5, 5],
               cols=[4, 5, 6, 5, 3, 4, 5, 3, 5], color=2),
      generate(height=11, rows=[1, 2, 2, 3, 4, 4, 4, 5],
               cols=[2, 2, 3, 3, 2, 3, 4, 4], color=1),
      generate(height=12, rows=[3, 3, 4, 4, 4, 4, 5, 5],
               cols=[4, 6, 3, 4, 5, 6, 6, 7], color=8),
  ]
  test = [
      generate(height=12, rows=[4, 4, 4, 4, 5, 6, 6, 7, 7, 7, 7],
               cols=[4, 5, 6, 7, 4, 2, 4, 2, 3, 4, 5], color=6),
  ]
  return {"train": train, "test": test}

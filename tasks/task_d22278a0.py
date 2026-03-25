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


def generate(size=None, rows=None, cols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
  """
  if size is None:
    size = common.randint(6, 18)
    corners = [(0, 0), (size - 1, 0), (0, size - 1), (size - 1, size - 1)]
    pixels = common.sample(corners, common.randint(2, 4))
    rows, cols = zip(*pixels)
    colors = common.random_colors(len(pixels))

  grid, output = common.grids(size, size)
  for row, col, color in zip(rows, cols, colors):
    grid[row][col] = color
  for r in range(size):
    for c in range(size):
      # Choose the (hopefully unique) minimal index.
      min_dist, min_idxs = size * size, []
      for idx, _ in enumerate(colors):
        row, col = rows[idx], cols[idx]
        dist = abs(row - r) +  abs(col - c)
        if min_dist > dist: min_dist, min_idxs = dist, []
        if min_dist == dist: min_idxs.append(idx)
      if len(min_idxs) > 1: continue
      idx = min_idxs[0]
      if max(abs(rows[idx] - r), abs(cols[idx] - c)) % 2: continue
      output[r][c] = colors[idx]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=10, rows=[0, 0], cols=[0, 9], colors=[1, 2]),
      generate(size=12, rows=[0, 11], cols=[11, 0], colors=[3, 8]),
      generate(size=13, rows=[0, 12], cols=[0, 0], colors=[2, 4]),
      generate(size=7, rows=[0, 0, 6], cols=[0, 6, 0], colors=[1, 2, 8]),
  ]
  test = [
      generate(size=17, rows=[0, 16, 16], cols=[0, 0, 16], colors=[4, 8, 1]),
  ]
  return {"train": train, "test": test}

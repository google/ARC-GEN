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


def generate(size=None, rows=None, cols=None, idxs=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices into the colors list
    colors: digits representing the colors to be used
  """
  if size is None:
    size = common.randint(3, 9)
    coords = []
    for r in range(size):
      for c in range(r):
        if common.randint(0, 1) == 0: continue
        coords.append((r, c))
    rows, cols = [p[0] for p in coords], [p[1] for p in coords]
    colors = common.random_colors(size - 2, exclude=[common.gray()])
    idxs = [common.randint(0, len(colors) - 1) for _ in coords]

  grid, output = common.grids(size, size)
  for i in range(size):
    output[i][i] = grid[i][i] = common.gray()
  for r, c, idx in zip(rows, cols, idxs):
    output[c][r] = grid[r][c] = colors[idx]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=3, rows=[1], cols=[0], idxs=[0], colors=[3]),
      generate(size=4, rows=[2, 3, 3], cols=[0, 0, 2], idxs=[0, 0, 1],
               colors=[6, 4]),
      generate(size=5, rows=[2, 2, 3, 4, 4], cols=[0, 1, 1, 1, 3],
               idxs=[0, 0, 1, 1, 2], colors=[8, 2, 1]),
  ]
  test = [
      generate(size=6, rows=[2, 2, 4, 4, 4, 5, 5], cols=[0, 1, 0, 2, 3, 0, 2],
               idxs=[0, 0, 1, 2, 2, 1, 3], colors=[3, 2, 8, 6]),
  ]
  return {"train": train, "test": test}

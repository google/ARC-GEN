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


def generate(rows=None, cols=None, idxs=None, width=3, height=4):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices into the colors list
    width: the width of the grid
    height: the height of the grid
  """
  if rows is None:
    rows, cols, idxs = [], [], []
    for idx in range(2):
      pixels = common.random_pixels(width, height)
      rows.extend([p[0] for p in pixels])
      cols.extend([p[1] for p in pixels])
      idxs.extend([idx] * len(pixels))

  grid = common.grid(2 * width + 1, height)
  output = common.grid(width, height)
  for r in range(height):
    grid[r][width] = common.blue()
  for r, c, idx in zip(rows, cols, idxs):
    color = common.gray() if idx else common.orange()
    grid[r][width + 1 + c if idx else c] = color
  for r in range(height):
    for c in range(width):
      if grid[r][c] > 0 or grid[r][width + 1 + c] > 0: continue
      output[r][c] = common.green()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 0, 1, 2, 2, 3, 3],
               cols=[0, 1, 0, 0, 0, 0, 2, 0, 1],
               idxs=[0, 0, 0, 1, 1, 1, 1, 1, 1]),
      generate(rows=[0, 0, 2, 2, 3, 3, 0, 2, 3, 3],
               cols=[0, 1, 0, 1, 1, 2, 0, 0, 0, 1],
               idxs=[0, 0, 0, 0, 0, 0, 1, 1, 1, 1]),
      generate(rows=[0, 0, 1, 2, 3, 0, 1, 1, 2, 2],
               cols=[1, 2, 2, 1, 2, 0, 1, 2, 0, 1],
               idxs=[0, 0, 0, 0, 0, 1, 1, 1, 1, 1]),
      generate(rows=[0, 0, 1, 1, 2, 0, 0, 1, 1, 1, 3, 3],
               cols=[0, 2, 0, 1, 1, 0, 1, 0, 1, 2, 0, 2],
               idxs=[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]),
      generate(rows=[0, 1, 3, 3, 3, 0, 1, 2, 2, 2, 3, 3, 3],
               cols=[0, 2, 0, 1, 2, 1, 0, 0, 1, 2, 0, 1, 2],
               idxs=[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]),
  ]
  test = [
      generate(rows=[1, 1, 1, 3, 0, 1, 1, 2, 3, 3, 3],
               cols=[0, 1, 2, 0, 1, 0, 1, 0, 0, 1, 2],
               idxs=[0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]),
  ]
  return {"train": train, "test": test}

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
    size: the width and height of the (square) grid
  """
  if rows is None:
    pixels = common.sample(common.all_pixels(size, size), 10)
    kept = []
    for p in pixels:
      keep = True
      for k in kept:
        keep = keep and (abs(p[0] - k[0]) >= 3 or abs(p[1] - k[1]) >= 3)
      if not keep: continue
      kept.append(p)
    rows, cols = [p[0] for p in kept], [p[1] for p in kept]

  grid, output = common.grids(size, size)
  for r, c in zip(rows, cols):
    output[r][c] = grid[r][c] = 1
    if r > 0:
      output[r - 1][c] = common.red()
    if r < size - 1:
      output[r + 1][c] = common.cyan()
    if c > 0:
      output[r][c - 1] = common.orange()
    if c < size - 1:
      output[r][c + 1] = common.pink()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[1, 3, 5, 7, 9], cols=[6, 9, 3, 7, 1]),
      generate(rows=[0, 2, 3, 5, 8, 9], cols=[5, 0, 9, 5, 2, 9]),
  ]
  test = [
      generate(rows=[0, 0, 2, 3, 6, 6, 9], cols=[1, 9, 7, 3, 7, 0, 4]),
  ]
  return {"train": train, "test": test}

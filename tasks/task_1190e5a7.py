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


def generate(rows=None, cols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of row thicknesses
    cols: a list of column thicknesses
    colors: a pair of colors
  """
  if rows is None:
    # We want to favor smaller values, so we'll use a large range and invert
    # the square roots.
    rows = [common.randint(1, 255) for _ in range(common.randint(2, 7))]
    cols = [common.randint(1, 255) for _ in range(common.randint(2, 7))]
    rows = [16 - int(common.sqrt(r)) for r in rows]
    cols = [16 - int(common.sqrt(c)) for c in cols]
    colors = common.random_colors(2)

  width = sum(cols) + len(cols) - 1
  height = sum(rows) + len(rows) - 1
  grid = common.grid(width, height, colors[0])
  output = common.grid(len(cols), len(rows), colors[0])
  r = -1
  for row in rows:
    r += row + 1
    if r >= height: break
    for c in range(width):
      grid[r][c] = colors[1]
  c = -1
  for col in cols:
    c += col + 1
    if c >= width: break
    for r in range(height):
      grid[r][c] = colors[1]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[2, 12], cols=[1, 8, 2, 1], colors=[3, 7]),
      generate(rows=[3, 5, 1], cols=[4, 6], colors=[1, 8]),
      generate(rows=[2, 4, 8, 4, 1, 3], cols=[6, 14, 1, 1, 1], colors=[3, 1]),
  ]
  test = [
      generate(rows=[2, 4, 4, 4, 4], cols=[15, 4, 1], colors=[1, 5]),
  ]
  return {"train": train, "test": test}

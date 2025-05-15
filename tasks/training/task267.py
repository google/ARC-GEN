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


def generate(rows=None, cols=None, colors=None, size=7):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) grid
  """
  if rows is None:
    pixels = common.continuous_creature(common.randint(12, 15), 5, 5)
    rows, cols = [p[0] + 1 for p in pixels], [p[1] + 1 for p in pixels]
    colors = common.random_colors(2)

  grid, output = common.grids(size, size)
  for r, c in zip(rows, cols):
    grid[r][c], output[r][c] = colors[0], colors[1]
  grid[6][0] = colors[1]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[1, 1, 1, 2, 3, 3, 3, 3, 4, 4, 4, 5],
               cols=[1, 2, 3, 2, 1, 2, 3, 4, 2, 3, 4, 3], colors=[2, 4]),
      generate(rows=[1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 5, 5],
               cols=[3, 2, 3, 4, 1, 2, 3, 4, 1, 2, 2, 3], colors=[3, 6]),
  ]
  test = [
      generate(rows=[1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 4, 4, 5, 5, 5],
               cols=[1, 2, 3, 1, 2, 3, 4, 5, 3, 4, 2, 3, 2, 3, 4],
               colors=[8, 2]),
  ]
  return {"train": train, "test": test}

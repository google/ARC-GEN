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


def generate(width=None, height=None, rows=None, cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
  """
  if width is None:
    width, height = common.randint(3, 6), common.randint(3, 6)
    pixels = common.random_pixels(width, height)
    rows, cols = zip(*pixels)

  grid, output = common.grids(width, height)
  for r, c in zip(rows, cols):
    grid[r][c] = common.green()
    output[r][c] = common.cyan()
  for pixel in common.edgefree_pixels(grid):
    output[pixel[0]][pixel[1]] = common.green()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=3, height=3, rows=[0, 0, 1, 2, 2], cols=[0, 1, 1, 0, 2]),
      generate(width=6, height=4, rows=[0, 0, 1, 1, 1, 2, 3],
               cols=[1, 5, 1, 2, 3, 4, 1]),
      generate(width=4, height=4, rows=[0, 0, 0, 1, 1, 2, 2, 3, 3],
               cols=[0, 1, 3, 0, 1, 0, 3, 2, 3]),
      generate(width=6, height=5, rows=[0, 0, 1, 1, 2, 3, 3, 4, 4, 4],
               cols=[0, 1, 1, 4, 0, 1, 2, 1, 2, 5]),
  ]
  test = [
      generate(width=5, height=5, rows=[0, 0, 0, 1, 1, 1, 2, 3, 3, 4, 4],
               cols=[0, 2, 4, 0, 1, 2, 4, 1, 2, 1, 2]),
  ]
  return {"train": train, "test": test}

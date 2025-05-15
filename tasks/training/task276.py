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
    width, height = common.randint(4, 6), common.randint(4, 6)
    pixels = common.random_pixels(width, height)
    rows, cols = zip(*pixels)

  grid = common.grid(width, height, common.pink())
  output = common.grid(width, height, common.red())
  for r, c in zip(rows, cols):
    output[r][c] = grid[r][c] = common.orange()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=4, height=3, rows=[0, 1, 1, 2, 2, 2],
               cols=[2, 2, 3, 0, 1, 3]),
      generate(width=4, height=6,
               rows=[0, 0, 0, 1, 2, 2, 2, 3, 3, 3, 4, 4, 5],
               cols=[0, 1, 2, 2, 0, 1, 3, 0, 2, 3, 0, 2, 3]),
      generate(width=6, height=3,
               rows=[0, 0, 1, 1, 1, 1, 2, 2, 2, 2],
               cols=[0, 1, 1, 3, 4, 5, 0, 2, 3, 5]),
  ]
  test = [
      generate(width=4, height=4,
               rows=[0, 0, 1, 1, 2, 2, 2, 3, 3],
               cols=[1, 2, 1, 3, 0, 1, 2, 0, 2]),
  ]
  return {"train": train, "test": test}

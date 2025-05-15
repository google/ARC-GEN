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


def generate(rows=None, cols=None, width=3, height=3):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    width: the width of one grid half
    height: the height of the grid
  """
  if rows is None:
    while True:
      pixels = common.random_pixels(2 * width + 1, height)
      if not [p for p in pixels if p[1] <= 2]: continue
      if not [p for p in pixels if p[1] >= 4]: continue
      break
    rows, cols = zip(*pixels)

  grid, output = common.grid_intersect(width, height, rows, cols,
                                       common.black(), common.gray(),
                                       common.blue(), common.black(),
                                       common.red())
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1, 2, 0, 1, 1, 1], cols=[0, 1, 0, 5, 4, 5, 6]),
      generate(rows=[0, 0, 1, 2, 2, 0, 1, 1, 1, 2],
               cols=[0, 1, 2, 0, 1, 5, 4, 5, 6, 5]),
      generate(rows=[0, 1, 1, 2, 2, 1, 1, 2, 2],
               cols=[2, 0, 1, 1, 2, 4, 6, 4, 6]),
  ]
  test = [
      generate(rows=[0, 0, 1, 2, 2, 0, 0, 1, 1, 2],
               cols=[0, 2, 1, 0, 2, 4, 6, 4, 6, 5]),
  ]
  return {"train": train, "test": test}

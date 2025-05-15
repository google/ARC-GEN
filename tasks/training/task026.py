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


def generate(rows=None, cols=None, width=3, height=5):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    width: the width of one grid half
    height: the height of the grid
  """
  if rows is None:
    pixels = common.random_pixels(2 * width + 1, height)
    rows, cols = zip(*pixels)

  grid, output = common.grid_intersect(width, height, rows, cols,
                                       common.black(), common.blue(),
                                       common.black(), common.maroon(),
                                       common.cyan())
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1, 1, 1, 2, 2, 3, 3, 3, 3, 3, 4],
               cols=[0, 0, 1, 6, 1, 6, 0, 1, 2, 5, 6, 0]),
      generate(rows=[0, 0, 0, 0, 0, 1, 2, 3, 3, 3, 4],
               cols=[0, 1, 2, 5, 6, 1, 0, 0, 1, 2, 0]),
      generate(rows=[0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 4, 4, 4, 4],
               cols=[1, 2, 5, 1, 2, 4, 6, 1, 2, 5, 6, 0, 4, 0, 1, 4, 6]),
      generate(rows=[0, 0, 1, 1, 1, 1, 3, 3, 3, 3, 3, 4, 4, 4, 4],
               cols=[0, 5, 1, 2, 5, 6, 0, 2, 4, 5, 6, 1, 2, 5, 6]),
      generate(rows=[0, 0, 1, 2, 2, 3, 3, 3, 3, 4, 4],
               cols=[0, 5, 1, 4, 5, 1, 2, 5, 6, 4, 5]),
  ]
  test = [
      generate(rows=[0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 4, 4],
               cols=[2, 4, 6, 0, 4, 5, 6, 2, 4, 6, 5, 0, 4]),
  ]
  return {"train": train, "test": test}

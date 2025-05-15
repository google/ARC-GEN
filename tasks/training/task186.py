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


def generate(rows=None, cols=None, size=3):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    size: the width and height of the (square) grid
  """
  if rows is None:
    count = common.randint(1, 4)
    pixels = common.sample(common.all_pixels(size, size), count)
    rows, cols = zip(*pixels)

  grid, output = common.grids(size, size)
  for r, c in zip(rows, cols):
    grid[r][c] = common.blue()
  output[0][0] = common.red() if len(rows) >= 1 else common.black()
  output[0][1] = common.red() if len(rows) >= 2 else common.black()
  output[0][2] = common.red() if len(rows) >= 3 else common.black()
  output[1][1] = common.red() if len(rows) >= 4 else common.black()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[1], cols=[0]),
      generate(rows=[1, 0], cols=[0, 1]),
      generate(rows=[2, 0], cols=[0, 2]),
      generate(rows=[0, 1], cols=[1, 2]),
      generate(rows=[0], cols=[2]),
      generate(rows=[0, 0, 2], cols=[0, 1, 0]),
      generate(rows=[0, 1, 1], cols=[1, 0, 1]),
      generate(rows=[0, 0, 2, 2], cols=[0, 1, 0, 2]),
      generate(rows=[0, 1, 1, 2], cols=[1, 0, 1, 0]),
      generate(rows=[0, 1, 2, 2], cols=[0, 2, 1, 2]),
  ]
  test = [
      generate(rows=[0, 2], cols=[1, 1]),
      generate(rows=[0, 1, 1, 2], cols=[1, 1, 2, 0]),
  ]
  return {"train": train, "test": test}

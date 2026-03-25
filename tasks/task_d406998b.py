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


def generate(rows=None, height=3):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    height: the height of grid
  """
  if rows is None:
    width = common.randint(10, 20)
    rows = [common.randint(0, height - 1) for _ in range(width)]

  width = len(rows)
  grid, output = common.grids(width, height)
  for c, r in enumerate(rows):
    grid[r][c] = common.gray()
    output[r][c] = common.green() if c % 2 != width % 2 else common.gray()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1, 0, 2, 1, 0, 2, 1, 2, 0]),
      generate(rows=[1, 0, 2, 0, 1, 2, 0, 1, 0, 2, 1, 2]),
      generate(rows=[1, 2, 0, 2, 1, 0, 1, 0, 2, 1, 2, 0, 1]),
      generate(rows=[1, 2, 0, 2, 1, 0, 2, 0, 1, 0, 1, 0, 2, 1]),
  ]
  test = [
      generate(rows=[1, 2, 1, 0, 2, 1, 2, 0, 1, 0, 2, 1, 0, 2, 0, 1, 2]),
  ]
  return {"train": train, "test": test}

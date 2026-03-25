# Copyright 2026 Google LLC
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


def generate(groups=None, rows=None, cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    groups: The groups of the pixels.
    rows: The rows of the pixels.
    cols: The columns of the groups.
  """

  if groups is None:
    groups, rows = [], []
    for group in range(4):
      pixels = common.randint(1, 4)
      groups.extend([group] * pixels)
      rows.extend(common.sample(range(10), pixels))
    cols = sorted(common.sample(range(10), 4))

  grid, output = common.grids(10, 10, 5)
  for group, row in zip(groups, rows):
    grid[row][cols[group]] = 0
    output[row][cols[group]] = group + 1
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(groups=[0, 1, 1, 1, 1, 2, 2, 3], rows=[0, 2, 4, 7, 9, 0, 3, 8],
               cols=[0, 4, 7, 8]),
      generate(groups=[0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3],
               rows=[3, 5, 6, 8, 4, 5, 6, 8, 0, 3, 4, 8, 7, 8, 9],
               cols=[1, 4, 5, 8]),
      generate(groups=[0, 1, 1, 2, 3, 3, 3, 3], rows=[0, 0, 7, 5, 3, 4, 5, 8],
               cols=[5, 6, 8, 9]),
  ]
  test = [
      generate(groups=[0, 0, 0, 1, 1, 2, 3, 3], rows=[3, 7, 9, 5, 6, 0, 4, 9],
               cols=[0, 2, 3, 5]),
  ]
  return {"train": train, "test": test}

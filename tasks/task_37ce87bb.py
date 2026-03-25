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


def generate(height=None, values=None):
  """Returns input and output grids according to the given parameters.

  Args:
    height: The height of the grid.
    values: The values of the grid.
  """

  if height is None:
    height = common.randint(6, 10)
    count = height - common.randint(3, 4)
    while True:
      values = [common.randint(-height + 1, height - 1) for _ in range(count)]
      if 0 in values: continue
      the_sum, good = 0, True
      for value in values:
        the_sum += value
        if the_sum < 0: good = False  # Don't allow negative accumulation.
      if the_sum <= 0 or the_sum >= height: good = False
      if good: break

  grid, output = common.grids(2 * len(values) + 3, height, 7)
  the_sum = 0
  for i, value in enumerate(values):
    for j in range(abs(value)):
      grid[height - 1 - j][2 * i + 1] = 8 if value > 0 else 2
      output[height - 1 - j][2 * i + 1] = 8 if value > 0 else 2
    the_sum += value
  for j in range(the_sum):
    output[height - 1 - j][2 * len(values) + 1] = 5
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(height=6, values=[5, -4]),
      generate(height=6, values=[2, 3]),
      generate(height=8, values=[2, 5, -6, 3]),
  ]
  test = [
      generate(height=9, values=[7, -3, 2, 5, -1, -8]),
  ]
  return {"train": train, "test": test}

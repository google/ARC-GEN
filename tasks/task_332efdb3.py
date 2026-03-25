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


def generate(size=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
  """

  if size is None:
    size = 2 * common.randint(1, 14) + 1

  grid, output = common.grids(size, size)
  for row in range(size):
    for col in range(size):
      output[row][col] = 1 if row % 2 == 0 or col % 2 == 0 else 0
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=5),
      generate(size=7),
      generate(size=9),
  ]
  test = [
      generate(size=11),
  ]
  return {"train": train, "test": test}

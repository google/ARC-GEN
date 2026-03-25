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


def generate(row=None, length=None):
  """Returns input and output grids according to the given parameters.

  Args:
    row: Row of the line.
    length: Length of the line.
  """

  if row is None:
    length = common.randint(1, 7)
    row = common.randint(0, 15 - length * 2)

  grid, output = common.grids(16, 16, 7)
  for i in range(length):
    grid[15 - row - i][row + i] = 2
  for i in range(length + 1):
    output[15 - row - i - length][row + i + length] = 2
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(row=1, length=2),
      generate(row=0, length=1),
      generate(row=3, length=3),
  ]
  test = [
      generate(row=6, length=4),
  ]
  return {"train": train, "test": test}

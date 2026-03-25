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


def generate(width=None, height=None, brow=None, bcol=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the box.
    height: The height of the box.
    brow: The row of the box.
    bcol: The column of the box.
  """

  if width is None:
    width, height = common.randint(3, 11), common.randint(3, 11)
    brow, bcol = common.randint(1, 12 - height), common.randint(1, 12 - width)

  grid, output = common.grids(13, 13)
  grid[brow][bcol] = grid[brow + height - 1][bcol + width - 1] = 2
  for r in range(height):
    for c in range(width):
      output[brow + r][bcol + c] = 1
  for i in range(13):
    output[brow][i] = output[brow + height - 1][i] = 2
    output[i][bcol] = output[i][bcol + width - 1] = 2
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=9, height=5, brow=4, bcol=2),
      generate(width=6, height=7, brow=3, bcol=3),
  ]
  test = [
      generate(width=6, height=10, brow=1, bcol=4),
  ]
  return {"train": train, "test": test}

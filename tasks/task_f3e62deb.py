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


def generate(row=None, col=None, color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    row: The row of the box.
    col: The column of the box.
    color: The color of the box.
  """

  if color is None:
    row, col = common.randint(2, 5), common.randint(2, 5)
    color = common.choice([3, 4, 6, 8])

  grid, output = common.grids(10, 10)
  common.hollow_rect(grid, 3, 3, row, col, color)
  if color == 3: col = 0
  if color == 4: row = 7
  if color == 6: row = 0
  if color == 8: col = 7
  common.hollow_rect(output, 3, 3, row, col, color)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(row=3, col=4, color=6),
      generate(row=4, col=2, color=6),
      generate(row=5, col=2, color=8),
      generate(row=2, col=3, color=4),
      generate(row=3, col=3, color=8),
      generate(row=2, col=2, color=8),
  ]
  test = [
      generate(row=5, col=3, color=3),
      generate(row=4, col=4, color=4),
  ]
  return {"train": train, "test": test}

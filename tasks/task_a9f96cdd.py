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


def generate(row=None, col=None, width=5, height=3):
  """Returns input and output grids according to the given parameters.

  Args:
    row: a vertical coordinate where the center should be placed
    col: a horizontal coordinate where the center should be placed
    width: the width of the grid
    height: the height of the grid
  """
  if row is None:
    row, col = common.randint(0, height - 1), common.randint(0, width - 1)

  grid, output = common.grids(width, height, common.black())
  common.draw(grid, row, col, common.red())
  common.draw(output, row - 1, col - 1, common.green())
  common.draw(output, row - 1, col + 1, common.pink())
  common.draw(output, row + 1, col - 1, common.cyan())
  common.draw(output, row + 1, col + 1, common.orange())
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(row=1, col=1),
      generate(row=2, col=4),
      generate(row=0, col=2),
      generate(row=1, col=3),
  ]
  test = [
      generate(row=1, col=4),
  ]
  return {"train": train, "test": test}

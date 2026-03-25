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


def generate(prow=None, pcol=None):
  """Returns input and output grids according to the given parameters.

  Args:
    prow: The row of the pixel.
    pcol: The column of the pixel.
  """

  if prow is None:
    prow, pcol = common.randint(0, 6), common.randint(0, 6)

  grid, output = common.grids(15, 15)
  for i in range(9):
    output[2][3 + i] = grid[2][3 + i] = 3
    output[10][3 + i] = grid[10][3 + i] = 3
    output[2 + i][3] = grid[2 + i][3] = 3
    output[2 + i][11] = grid[2 + i][11] = 3
  for r in range(7):
    for c in range(7):
      max_mod = max(abs(prow - r), abs(pcol - c)) % 2
      output[3 + r][4 + c] = 2 if max_mod == 0 else 4
  output[prow + 3][pcol + 4] = grid[prow + 3][pcol + 4] = 3
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(prow=5, pcol=1),
      generate(prow=3, pcol=3),
      generate(prow=0, pcol=5),
  ]
  test = [
      generate(prow=2, pcol=0),
  ]
  return {"train": train, "test": test}

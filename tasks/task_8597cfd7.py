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


def generate(height=None, reds=None, yellows=None):
  """Returns input and output grids according to the given parameters.

  Args:
    height: The height of the grid.
    reds: The number of red cells in each half.
    yellows: The number of yellow cells in each half.
  """

  def draw():
    if reds[0] >= reds[1] or yellows[0] >= yellows[1]: return None, None
    if reds[1] - reds[0] == yellows[1] - yellows[0]: return None, None
    bgcolor = 2 if (reds[1] - reds[0]) > (yellows[1] - yellows[0]) else 4
    grid, output = common.grid(9, height), common.grid(2, 2, bgcolor)
    for c in range(9):
      grid[height // 2][c] = 5
    for i in range(2):
      for r in range(reds[i]):
        grid[i * (height // 2 + 1) + r][2] = 2
      for r in range(yellows[i]):
        grid[i * (height // 2 + 1) + r][6] = 4
    return grid, output

  if reds is None:
    height = 9 if common.randint(0, 1) else 11
    max_tall = height // 2
    while True:
      reds = [common.randint(1, max_tall), common.randint(1, max_tall)]
      yellows = [common.randint(1, max_tall), common.randint(1, max_tall)]
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(height=11, reds=[1, 4], yellows=[3, 5]),
      generate(height=9, reds=[1, 4], yellows=[2, 4]),
      generate(height=11, reds=[2, 4], yellows=[2, 3]),
      generate(height=9, reds=[1, 2], yellows=[2, 4]),
  ]
  test = [
      generate(height=11, reds=[3, 4], yellows=[2, 4]),
  ]
  return {"train": train, "test": test}

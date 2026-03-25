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


def generate(size=None, angle=None, val=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    rows: The rows of the boxes.
    cols: The columns of the boxes.
    thicks: The thicknesses of the boxes.
  """

  if size is None:
    size = common.randint(8, 18)
    colors = [common.randint(0, 1) for _ in range(size * size)]
    angle = common.randint(0, 3)
    val = common.randint(1, size - 2)

  grid, output = common.grids(size, size)
  for i, color in enumerate(colors):
    output[i // size][i % size] = grid[i // size][i % size] = color
  if angle == 0:
    for c in range(size):
      output[val][c] = 3 if output[val][c] else 2
    output[val][0] = output[val][size - 1] = grid[val][0] = grid[val][size - 1] = 2
  if angle == 1:
    for r in range(size):
      output[r][val] = 3 if output[r][val] else 2
    output[0][val] = output[size - 1][val] = grid[0][val] = grid[size - 1][val] = 2
  if angle == 2:
    for i in range(size):
      output[i][i] = 3 if output[i][i] else 2
    output[0][0] = output[size - 1][size - 1] = grid[0][0] = grid[size - 1][size - 1] = 2
  if angle == 3:
    for i in range(size):
      output[i][size - 1 - i] = 3 if output[i][size - 1 - i] else 2
    output[0][size - 1] = output[size - 1][0] = grid[0][size - 1] = grid[size - 1][0] = 2
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=12, angle=0, val=8,
               colors=[0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
                       0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0,
                       0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0,
                       0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0,
                       1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1,
                       1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0,
                       1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0,
                       0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0,
                       1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1,
                       0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0]),
      generate(size=16, angle=2, val=0,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0,
                       0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0,
                       0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1,
                       0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0,
                       0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1,
                       0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0,
                       0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0,
                       1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1,
                       1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0,
                       0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1,
                       0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0,
                       1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1,
                       0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1,
                       0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0]),
      generate(size=10, angle=1, val=6,
               colors=[0, 1, 1, 1, 0, 0, 0, 0, 0, 1,
                       1, 0, 1, 0, 1, 1, 1, 0, 1, 1,
                       0, 0, 0, 0, 0, 0, 0, 0, 1, 0,
                       0, 1, 0, 0, 0, 0, 1, 1, 1, 0,
                       1, 1, 1, 0, 0, 0, 1, 0, 0, 1,
                       1, 1, 1, 1, 1, 1, 0, 0, 1, 0,
                       0, 1, 1, 0, 1, 0, 1, 0, 1, 0,
                       1, 0, 0, 0, 1, 0, 1, 1, 0, 1,
                       0, 1, 1, 1, 1, 0, 0, 1, 1, 1,
                       0, 1, 0, 1, 0, 0, 0, 1, 1, 0]),
  ]
  test = [
      generate(size=18, angle=3, val=0,
               colors=[1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0,
                       1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1,
                       0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0,
                       1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1,
                       0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0,
                       1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1,
                       1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1,
                       1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1,
                       0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0,
                       1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0,
                       0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0,
                       0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1,
                       1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1,
                       1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
                       1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 
                       1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0,
                       1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1,
                       0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0]),
  ]
  return {"train": train, "test": test}

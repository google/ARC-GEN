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


def generate(length=None, brow=None, bcol=None, dogear=None):
  """Returns input and output grids according to the given parameters.

  Args:
    length: The length of the box.
    brow: The row of the box.
    bcol: The column of the box.
    dogear: The dogear of the box.
  """

  if length is None:
    length = common.randint(4, 8)
    brow, bcol = common.randint(0, 8 - length), common.randint(0, 8 - length)
    dogear = common.randint(0, 3)

  grid, output = common.grids(8, 8, 7)
  points = [[brow, bcol],
            [brow, bcol + length - 1],
            [brow + length - 1, bcol],
            [brow + length - 1, bcol + length - 1]]
  dr = 1 if dogear in [0, 1] else -1
  dc = 1 if dogear in [0, 2] else -1
  points[dogear][0] += dr
  points[dogear][1] += dc
  srow = brow if dogear in [0, 1] else (brow + length - 1)
  scol = bcol if dogear in [0, 2] else (bcol + length - 1)
  for row in range(brow, brow + length):
    output[row][scol] = 8
  for col in range(bcol, bcol + length):
    output[srow][col] = 8
  for i in range(length):
    r, c = brow + i, (bcol + i) if dogear in [1, 2] else (bcol + length - 1 - i)
    output[r][c] = 8
  for point in points:
    output[point[0]][point[1]] = grid[point[0]][point[1]] = 5
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(length=4, brow=0, bcol=0, dogear=2),
      generate(length=6, brow=1, bcol=1, dogear=3),
      generate(length=8, brow=0, bcol=0, dogear=0),
  ]
  test = [
      generate(length=7, brow=0, bcol=1, dogear=1),
  ]
  return {"train": train, "test": test}

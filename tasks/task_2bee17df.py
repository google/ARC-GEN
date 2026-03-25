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


def generate(size=None, numred=None, flip=None, xpose=None, lengths=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    numred: the number of red columns
    flip: whether to flip the grid
    xpose: whether to transpose the grid
    lengths: the lengths of the columns
  """
  if size is None:
    size = 2 * common.randint(5, 7)
    numred = common.randint(5 * size // 3, 7 * size // 3)
    lengths = [max(1, common.randint(0, 3)) for _ in range(4 * size)]
    flip, xpose = common.randint(0, 1), common.randint(0, 1)

  grid, output = common.grids(size, size)
  idx = 0
  for c in range(size):
    for r in range(lengths[idx]):
      color = common.red() if idx < numred else common.cyan()
      output[r][c] = grid[r][c] = color
    idx += 1
  for r in range(size):
    for c in range(size - lengths[idx], size):
      color = common.red() if idx < numred else common.cyan()
      output[r][c] = grid[r][c] = color
    idx += 1
  for c in range(size - 1, -1, -1):
    for r in range(size - lengths[idx], size):
      color = common.red() if idx < numred else common.cyan()
      output[r][c] = grid[r][c] = color
    idx += 1
  for r in range(size - 1, -1, -1):
    for c in range(lengths[idx]):
      color = common.red() if idx < numred else common.cyan()
      output[r][c] = grid[r][c] = color
    idx += 1
  for r in range(1, size - 1):
    free = True
    for c in range(1, size - 1):
      if grid[r][c]: free = False
    if not free: continue
    for c in range(1, size - 1):
      output[r][c] = common.green()
  for c in range(1, size - 1):
    free = True
    for r in range(1, size - 1):
      if grid[r][c]: free = False
    if not free: continue
    for r in range(1, size - 1):
      output[r][c] = common.green()
  if flip: grid, output = grid[::-1], output[::-1]
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=12, numred=19, flip=0, xpose=0,
               lengths=[1, 1, 1, 1, 2, 3, 1, 2, 3, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1,
                        1, 1, 1, 1, 1, 1, 2, 1, 1, 3, 3, 2, 1, 1, 2, 3, 1, 1, 3,
                        2, 1, 1, 1, 1, 1, 1, 1, 1, 0]),
      generate(size=12, numred=27, flip=0, xpose=1,
               lengths=[0, 1, 2, 1, 1, 3, 2, 2, 1, 1, 2, 2, 2, 2, 1, 2, 1, 1, 2,
                        1, 1, 2, 3, 3, 3, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2,
                        2, 3, 4, 2, 1, 1, 1, 1, 1, 1]),
      generate(size=10, numred=20, flip=1, xpose=0,
               lengths=[0, 2, 1, 1, 1, 2, 3, 3, 2, 2, 2, 2, 1, 1, 1, 2, 2, 1, 1,
                        1, 0, 1, 2, 1, 2, 3, 1, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1,
                        1, 1, 1]),
  ]
  test = [
      generate(size=14, numred=27, flip=1, xpose=0,
               lengths=[0, 1, 1, 2, 1, 2, 2, 1, 1, 1, 1, 2, 3, 3, 3, 3, 2, 1, 1,
                        1, 1, 1, 3, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 2, 2, 1, 1,
                        2, 3, 3, 3, 3, 3, 3, 1, 3, 2, 1, 2, 2, 2, 1, 2, 2, 1]),
  ]
  return {"train": train, "test": test}

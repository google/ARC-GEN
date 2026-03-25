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


def generate(size=None, grows=None, prows=None, lengths=None, flop=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    grows: The rows of the grippers.
    prows: The rows of the pixels.
    lengths: The lengths of the pixels.
    flop: Whether to flop the grids.
    xpose: Whether to transpose the grids.
  """

  if size is None:
    size = 2 * common.randint(4, 10)
    grow, grows = common.randint(1, 3), []
    while grow + 1 < size:
      grows.append(grow)
      grow += common.randint(4, 6)
    prow, prows, lengths = common.randint(0, 1), [], []
    while True:
      if prow - 1 in grows or prow + 1 in grows: prow += 1
      if prow >= size: break
      prows.append(prow)
      lengths.append(common.randint(1, 2))
      prow += common.randint(2, 4)
    flop, xpose = common.randint(0, 1), common.randint(0, 1)

  grid, output = common.grids(size, size, 7)
  for grow in grows:
    for col in range(3):
      grid[grow - 1][col] = grid[grow + 1][col] = 0
      output[grow - 1][size - 1 - col] = output[grow + 1][size - 1 - col] = 0
    for col in range(2, size):
      grid[grow][col] = 0
    output[grow][size - 1] = 0
  for prow, length in zip(prows, lengths):
    for col in range(length):
      grid[prow][col] = 9
      output[prow][col if prow not in grows else (size - 3 + col)] = 9
  if flop: grid, output = common.flop(grid), common.flop(output)
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=14, grows=[3, 8, 12], prows=[0, 3, 6, 12],
               lengths=[1, 1, 2, 1], flop=False, xpose=False),
      generate(size=8, grows=[2, 6], prows=[2, 4], lengths=[1, 1], flop=True,
               xpose=True),
      generate(size=16, grows=[1, 5, 11], prows=[1, 5, 9, 14],
               lengths=[1, 2, 1, 2], flop=True, xpose=False),
  ]
  test = [
      generate(size=20, grows=[2, 7, 11, 16], prows=[0, 4, 7, 11, 14, 16, 18],
               lengths=[1, 1, 1, 2, 2, 2, 2], flop=False, xpose=True),
  ]
  return {"train": train, "test": test}

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


def generate(size=None, pcolor=None, prows=None, pcols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the input grid.
    pcolor: The color of the pixels.
    prows: The rows of the pixels.
    pcols: The columns of the pixels.
  """

  if size is None:
    size = common.randint(4, 7)
    pcolor = common.random_color(exclude=[3])
    prows, pcols = [1], [common.randint(0, size - 1)]
    pcol = common.randint(0, size - 1)
    if size == 6 and pcol not in pcols:
      pcols.append(pcol)
      prows.append(4)

  grid, output = common.grid(size, size), common.grid(2 * size, 2 * size)
  for prow, pcol in zip(prows, pcols):
    grid[prow - 1][pcol] = grid[prow + 1][pcol] = pcolor
    output[prow - 1][pcol] = output[prow + 1][pcol] = pcolor
    output[prow - 1 + size][pcol + size] = output[prow + 1 + size][pcol + size] = pcolor
    for c in range(2 * size):
      output[prow][c] = 3
      output[prow + size][c] = 3
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=3, pcolor=8, prows=[1], pcols=[1]),
      generate(size=6, pcolor=4, prows=[1, 4], pcols=[1, 4]),
      generate(size=7, pcolor=7, prows=[1], pcols=[2]),
  ]
  test = [
      generate(size=4, pcolor=9, prows=[1], pcols=[0]),
  ]
  return {"train": train, "test": test}

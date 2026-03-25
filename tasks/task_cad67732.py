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


def generate(size=None, diag=None, offdiag=None, flop=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the input grid.
    diag: The diagonal values.
    offdiag: The off-diagonal values.
    flop: Whether to flop the input and output grids.
  """

  if size is None:
    while True:
      size = common.randint(5, 10)
      subset = common.random_colors(4)
      diag = common.choices(subset, 2)
      offdiag = common.choices(subset + [0], 2)
      if size > 5 and 0 not in offdiag and common.randint(0, 1):
        diag = [diag[0], diag[1], diag[1]]
        offdiag = [offdiag[0], offdiag[0], offdiag[1]]
      if len(set(diag + offdiag)) >= 3: break
    flop = common.randint(0, 1)

  grid, output = common.grid(size, size), common.grid(2 * size, 2 * size)
  for i in range(size):
    grid[i][i] = diag[i % len(diag)]
    if i + 1 < size:
      grid[i][i + 1] = grid[i + 1][i] = offdiag[(i + 1) % len(offdiag)]
  for i in range(2 * size):
    output[i][i] = diag[i % len(diag)]
    if i + 1 < 2 * size:
      output[i][i + 1] = output[i + 1][i] = offdiag[(i + 1) % len(offdiag)]
  if flop: grid, output = common.flop(grid), common.flop(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=5, diag=[2, 2], offdiag=[0, 5], flop=False),
      generate(size=6, diag=[4, 3, 3], offdiag=[1, 1, 2], flop=False),
      generate(size=8, diag=[1, 6], offdiag=[0, 0], flop=True),
  ]
  test = [
      generate(size=10, diag=[6, 8], offdiag=[4, 6], flop=True),
  ]
  return {"train": train, "test": test}

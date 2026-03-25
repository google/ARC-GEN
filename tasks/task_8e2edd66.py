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


def generate(vals=None, color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    vals: The values of the pixels.
    color: The color of the grid.
  """

  if vals is None:
    color = common.random_color()
    while True:
      vals = [1 if common.randint(0, 1) else 0 for _ in range(9)]
      if sum(vals) != 0: break

  grid, output = common.grid(3, 3), common.grid(9, 9)
  for i, val in enumerate(vals):
    grid[i // 3][i % 3] = val * color
    if val: continue
    for j, val2 in enumerate(vals):
      output[3 * (j // 3) + i // 3][3 * (j % 3) + i % 3] = (1 - val2) * color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(vals=[1, 1, 0, 0, 1, 1, 0, 1, 0], color=8),
      generate(vals=[1, 1, 0, 0, 0, 1, 0, 1, 0], color=9),
      generate(vals=[1, 0, 1, 1, 1, 1, 0, 1, 0], color=7),
  ]
  test = [
      generate(vals=[1, 1, 0, 0, 1, 0, 1, 0, 1], color=1),
  ]
  return {"train": train, "test": test}

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


def generate(values=None, color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    values: A list of integers.
    color: A color.
  """

  if values is None:
    color = common.choice([8, 3, 5])
    while True:
      values = [common.randint(0, 1) for _ in range(9)]
      if sum(values) > 0: break

  themap = {8: 2, 3: 1, 5: 4}
  grid, output = common.grids(3, 3)
  for i, val in enumerate(values):
    grid[i // 3][i % 3] = color if val else 0
    if not val: output[i // 3][i % 3] = themap[color]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(values=[1, 1, 1, 0, 0, 1, 0, 0, 0], color=5),
      generate(values=[0, 1, 0, 0, 1, 0, 1, 0, 0], color=8),
      generate(values=[1, 0, 1, 0, 1, 0, 0, 1, 0], color=8),
      generate(values=[0, 0, 1, 0, 1, 0, 1, 0, 0], color=3),
      generate(values=[1, 0, 0, 1, 1, 0, 1, 0, 0], color=5),
      generate(values=[1, 0, 0, 0, 1, 0, 0, 0, 0], color=8),
  ]
  test = [
      generate(values=[0, 1, 0, 1, 1, 0, 0, 0, 1], color=5),
      generate(values=[1, 0, 0, 1, 1, 1, 0, 0, 1], color=3),
  ]
  return {"train": train, "test": test}

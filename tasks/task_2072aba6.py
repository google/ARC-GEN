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


def generate(colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
  """

  if colors is None:
    while True:
      colors = [common.randint(0, 1) for _ in range(5)]
      if sum(colors) >= 3 and sum(colors) <= 6: break

  grid, output = common.grid(3, 3), common.grid(6, 6)
  for i, color in enumerate(colors):
    grid[i // 3][i % 3] = 5 * color
    if not color: continue
    output[2 * (i // 3)][2 * (i % 3)] = 1
    output[2 * (i // 3) + 1][2 * (i % 3)] = 2
    output[2 * (i // 3) + 1][2 * (i % 3) + 1] = 1
    output[2 * (i // 3)][2 * (i % 3) + 1] = 2
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[1, 0, 0, 0, 1, 0, 0, 0, 1]),
      generate(colors=[0, 1, 0, 1, 1, 1, 0, 1, 0]),
      generate(colors=[0, 1, 0, 0, 1, 1, 1, 1, 0]),
  ]
  test = [
      generate(colors=[0, 0, 0, 0, 1, 0, 1, 1, 1]),
  ]
  return {"train": train, "test": test}

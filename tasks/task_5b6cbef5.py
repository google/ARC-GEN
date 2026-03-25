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
    colors: The colors of the pixels.
  """

  if colors is None:
    color = common.randint(1, 4)
    while True:
      colors = [color if common.randint(0, 1) else 0 for _ in range(16)]
      if sum(colors) != 0: break

  grid, output = common.grid(4, 4), common.grid(16, 16)
  for i, color in enumerate(colors):
    grid[i // 4][i % 4] = color
    if not color: continue
    for j, color2 in enumerate(colors):
      output[4 * (j // 4) + i // 4][4 * (j % 4) + i % 4] = color2
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[3, 3, 0, 3, 3, 0, 0, 3, 0, 0, 0, 3, 3, 3, 0, 3]),
      generate(colors=[0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]),
      generate(colors=[0, 0, 0, 0, 4, 4, 4, 4, 0, 4, 4, 0, 4, 4, 0, 0]),
      generate(colors=[1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1]),
      generate(colors=[2, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 2, 0, 2, 0, 2]),
  ]
  test = [
      generate(colors=[0, 2, 0, 2, 2, 2, 0, 2, 2, 2, 0, 0, 0, 0, 0, 2]),
  ]
  return {"train": train, "test": test}

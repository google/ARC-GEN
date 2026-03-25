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
    colors = [common.choice([5, 7, 8]) for _ in range(9)]

  grid, output = common.grid(3, 3), common.grid(12, 3)
  for i, color in enumerate(colors):
    grid[i // 3][i % 3] = color
    output[i // 3][2 - i % 3] = color
    output[i // 3][3 + i % 3] = color
    output[i // 3][8 - i % 3] = color
    output[i // 3][9 + i % 3] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[8, 8, 8, 5, 5, 7, 5, 7, 8]),
      generate(colors=[7, 7, 8, 5, 8, 8, 5, 8, 8]),
      generate(colors=[8, 8, 7, 7, 5, 5, 5, 7, 8]),
      generate(colors=[7, 5, 7, 5, 5, 7, 7, 7, 5]),
  ]
  test = [
      generate(colors=[8, 5, 7, 5, 7, 5, 8, 8, 5]),
  ]
  return {"train": train, "test": test}

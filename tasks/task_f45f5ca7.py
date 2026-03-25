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
    while True:
      colors = [common.choice([0, 2, 3, 4, 8]) for _ in range(10)]
      if len(set(colors)) == 5: break

  grid, output = common.grids(10, 10)
  offsets = [0, 0, 2, 4, 3, 0, 0, 0, 1, 0]
  for row, color in enumerate(colors):
    grid[row][0] = color
    col = offsets[color]
    output[row][col] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[2, 8, 0, 3, 2, 4, 0, 8, 0, 3]),
      generate(colors=[3, 4, 2, 3, 0, 4, 8, 2, 0, 0]),
      generate(colors=[8, 3, 2, 4, 3, 8, 0, 3, 8, 0]),
  ]
  test = [
      generate(colors=[2, 4, 3, 2, 0, 8, 3, 0, 4, 2]),
  ]
  return {"train": train, "test": test}

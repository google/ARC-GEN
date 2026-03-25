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


def generate(width=None, colors=None, height=5):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    colors: a list of colors to be used in the input grid
    height: half the height of the input grid
  """
  if width is None:
    width = common.randint(2, 10)
    colors = [common.random_color() for _ in range(common.randint(2, 4))]

  grid, output = common.grids(width, 2 * height)
  for r, color in enumerate(colors):
    for c in range(width):
      output[2 * height - r - 1][c] = output[r][c] = grid[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=3, colors=[2, 2, 3]),
      generate(width=5, colors=[2, 8]),
  ]
  test = [
      generate(width=6, colors=[3, 5, 5]),
  ]
  return {"train": train, "test": test}

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


def generate(width=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    colors: The colors of the grid.
  """

  if width is None:
    width = 19 if common.randint(0, 1) else 29
    colors = common.random_colors(common.randint(2, 3))

  grid, output = common.grids(width, 3)
  grid[1][0], grid[1][1] = colors[0], colors[1]
  if len(colors) == 3: grid[1][3] = colors[2]
  for i, col in enumerate([0, 1, 3, 6, 10, 15, 21, 28]):
    common.draw(output, 1, col, colors[i % len(colors)])
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=19, colors=[6, 8, 1]),
      generate(width=29, colors=[2, 3]),
      generate(width=19, colors=[1, 2]),
  ]
  test = [
      generate(width=29, colors=[2, 1, 8]),
  ]
  return {"train": train, "test": test}

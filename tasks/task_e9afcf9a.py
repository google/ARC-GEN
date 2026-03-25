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


def generate(colors=None, width=6, height=2):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: digits representing the colors to be used
    width: width of the input grid
    height: height of the input grid
  """
  if colors is None:
    colors = common.random_colors(2)

  grid, output = common.grids(width, height)
  for c in range(width):
    for r in range(height):
      output[(r + c) % 2][c] = grid[r][c] = colors[r]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[3, 9]),
      generate(colors=[4, 8]),
  ]
  test = [
      generate(colors=[6, 2]),
  ]
  return {"train": train, "test": test}

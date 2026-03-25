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


def generate(width=None, height=None, left=None, right=None, color=None,
             xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: width of the grid.
    height: height of the grid.
    left: the left color
    right: the right color
    color: the main color
    xpose: whether to transpose the grid
  """

  if height is None:
    width, height = common.randint(12, 24), common.randint(3, 6)
    colors = common.random_colors(3)
    left, right, color = colors[0], colors[1], colors[2]
    xpose = common.randint(0, 1)

  grid, output = common.grids(width, height, color)
  common.rect(grid, 2, height - 2, 1, 1, left)
  common.rect(grid, 2, height - 2, 1, width - 3, right)
  common.rect(output, 2, height - 2, 1, 1, left)
  common.rect(output, 2, height - 2, 1, width - 3, right)
  common.rect(output, width // 2 - 3, height, 0, 3, left)
  common.rect(output, width // 2 - 3, height, 0, (width - 1) // 2 + 1, right)
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=16, height=5, left=1, right=6, color=4, xpose=False),
      generate(width=17, height=4, left=1, right=3, color=2, xpose=False),
      generate(width=19, height=3, left=2, right=1, color=8, xpose=True),
  ]
  test = [
      generate(width=22, height=3, left=8, right=1, color=2, xpose=True),
      generate(width=17, height=6, left=8, right=2, color=3, xpose=True),
  ]
  return {"train": train, "test": test}

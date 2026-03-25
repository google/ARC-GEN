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


def generate(width=None, height=None, color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the input grid.
    height: The height of the input grid.
    color: The color of the pixel.
  """

  if color is None:
    width, height = 2 * common.randint(1, 4) + 1, 2 * common.randint(1, 4) + 1
    color = common.random_color()

  grid, output = common.grids(width, height)
  grid[height // 2][width // 2] = color
  common.hollow_rect(output, width, height, 0, 0, color)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=7, height=5, color=1),
      generate(width=3, height=5, color=3),
      generate(width=5, height=5, color=6),
      generate(width=3, height=3, color=2),
  ]
  test = [
      generate(width=7, height=9, color=8),
  ]
  return {"train": train, "test": test}

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


def generate(width=None, length=None, color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    length: the length of the topmost line
    color: a digit representing a color to be used
  """
  if width is None:
    width = 2 * common.randint(3, 9)
    length = common.randint(1, width // 2 + 1)
    color = common.random_color()

  height = width // 2
  grid, output = common.grid(width, 1), common.grid(width, height)
  for c in range(length):
    grid[0][c] = color
  for r in range(height):
    for c in range(length + r):
      output[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=6, length=2, color=1),
      generate(width=8, length=1, color=2),
      generate(width=10, length=3, color=5),
      generate(width=6, length=4, color=8),
      generate(width=6, length=1, color=7),
  ]
  test = [
      generate(width=12, length=3, color=1),
  ]
  return {"train": train, "test": test}

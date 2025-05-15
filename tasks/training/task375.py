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


def generate(size=None, color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    color: a digit representing a color to be used
  """
  if size is None:
    size = 2 * common.randint(2, 7) + 1
    color = common.random_color()

  grid, output = common.grids(size, size, color)
  grid[size // 2][size // 2] = common.black()
  for i in range(size):
    output[i][i] = common.black()
    output[i][size - 1 - i] = common.black()
    output[size - 1 - i][i] = common.black()
    output[size - 1 - i][size - 1 - i] = common.black()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=3, color=1),
      generate(size=5, color=2),
      generate(size=7, color=3),
  ]
  test = [
      generate(size=11, color=6),
  ]
  return {"train": train, "test": test}

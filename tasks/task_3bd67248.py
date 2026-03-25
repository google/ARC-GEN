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
    color: a digit representing the left column color
  """
  if size is None:
    size = common.randint(3, 21)
    color = common.randint(1, 9)

  grid, output = common.grids(size, size)
  for r in range(size):
    output[r][0] = grid[r][0] = color
  for c in range(1, size):
    output[size - 1][c] = common.yellow()
    output[size - 1 - c][c] = common.red()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=15, color=6),
      generate(size=3, color=5),
      generate(size=7, color=8),
  ]
  test = [
      generate(size=10, color=3),
  ]
  return {"train": train, "test": test}

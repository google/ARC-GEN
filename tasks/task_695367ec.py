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


def generate(size=None, color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    color: The color of the grid.
  """

  if size is None:
    size, color = common.randint(2, 5), common.random_color()

  grid, output = common.grid(size, size, color), common.grid(15, 15)
  for r in range(15):
    for c in range(15):
      if r % (size + 1) == size or c % (size + 1) == size:
        output[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=2, color=8),
      generate(size=3, color=3),
      generate(size=4, color=2),
  ]
  test = [
      generate(size=5, color=4),
  ]
  return {"train": train, "test": test}

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
    colors: A list of colors to use.
  """

  if colors is None:
    colors = [common.random_color() for _ in range(4)]

  grid, output = common.grid(2, 2), common.grid(6, 6)
  for i, color in enumerate(colors):
    grid[i // 2][i % 2] = color
    for row in range(3):
      for col in range(3):
        r = row * 2 + i // 2
        c = col * 2 + ((1 - i % 2) if row % 2 else (i % 2))
        output[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[7, 9, 4, 3]),
      generate(colors=[8, 6, 6, 4]),
  ]
  test = [
      generate(colors=[3, 2, 7, 8]),
  ]
  return {"train": train, "test": test}

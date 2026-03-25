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
    num_colors = common.randint(1, 5)
    subset = common.random_colors(num_colors)
    while True:
      colors = common.choices(subset, 9)
      if len(set(colors)) == num_colors: break

  grid = common.grid(3, 3)
  for i, color in enumerate(colors):
    grid[i // 3][i % 3] = color
  output = common.upsample(grid, len(set(colors)))
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[4, 4, 7, 8, 7, 7, 8, 8, 4]),
      generate(colors=[8, 8, 8, 8, 8, 8, 8, 8, 8]),
      generate(colors=[3, 3, 3, 3, 3, 3, 3, 3, 3]),
      generate(colors=[4, 2, 8, 2, 2, 5, 8, 5, 4]),
      generate(colors=[2, 2, 4, 4, 4, 4, 2, 4, 2]),
      generate(colors=[1, 1, 1, 6, 6, 6, 6, 1, 6]),
      generate(colors=[3, 6, 6, 3, 6, 6, 3, 3, 3]),
  ]
  test = [
      generate(colors=[7, 1, 7, 3, 3, 6, 8, 8, 6]),
  ]
  return {"train": train, "test": test}

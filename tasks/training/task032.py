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


def generate(colors=None, active=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of digits representing different colors
    active: a list for each color, indicating which rows that color is active
  """
  if colors is None:
    size = common.randint(4, 6)
    colors = common.random_colors(size)
    while True:
      counts = common.choices(range((size + 3) // 2), k=size)
      active = [common.sample(range(size), count) for count in counts]
      if sum([len(c) for c in active]) >= size: break

  size = len(colors)
  grid, output = common.grids(size, size)
  for c in range(size):
    for r in range(len(active[c])):
      output[size - r - 1][c] = grid[active[c][r]][c] = colors[c]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[1, 4, 6, 9], active=[[3], [0, 2], [2], [0]]),
      generate(colors=[4, 0, 7, 8, 0, 9],
               active=[[3, 4, 5], [], [4, 5], [1, 4], [], [0]]),
      generate(colors=[6, 3, 0, 1, 2],
               active=[[3], [1, 2, 4], [], [0, 2], [2]]),
  ]
  test = [
      generate(colors=[5, 2, 6, 4, 3],
               active=[[1, 3, 4], [0, 3], [2], [0, 3], [0]]),
  ]
  return {"train": train, "test": test}

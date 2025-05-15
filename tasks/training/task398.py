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


def generate(colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of digits representing the colors to be used
  """
  if colors is None:
    colors = common.random_colors(common.randint(1, 5))
    colors.extend([0] * (5 - len(colors)))
    colors = common.shuffle(colors)

  num_colors = sum([1 for c in colors if c > 0])
  size = num_colors * len(colors)
  grid, output = common.grid(len(colors), 1), common.grid(size, size)
  for c, color in enumerate(colors):
    grid[0][c] = color
    for r in range(c, size):
      output[r][size - 1 + c - r] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[1, 0, 7, 0, 0]),
      generate(colors=[0, 0, 2, 0, 0]),
      generate(colors=[4, 0, 6, 0, 8]),
      generate(colors=[0, 9, 0, 8, 4]),
      generate(colors=[0, 4, 0, 0, 0]),
  ]
  test = [
      generate(colors=[0, 6, 7, 8, 9]),
  ]
  return {"train": train, "test": test}

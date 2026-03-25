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


def generate(colors=None, size=5):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) grid
  """
  if colors is None:
    colors = [common.random_color()]
    for _ in range(common.randint(3, 4)):
      color = colors[-1] if common.randint(0, 1) else common.random_color()
      colors.append(color)

  grid, output = common.grid(size, size), common.grid(2 * size, 2 * size)
  for r in range(size):
    for c in range(size):
      if max(r, c) < len(colors): grid[r][c] = colors[max(c, r)]
  for r in range(2 * size):
    for c in range(2 * size):
      output[r][c] = colors[max(c, r) % len(colors)]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[2, 2, 2, 3]),
      generate(colors=[1, 1, 4, 6]),
      generate(colors=[2, 3, 4, 1, 6]),
  ]
  test = [
      generate(colors=[7, 7, 3, 2, 2]),
  ]
  return {"train": train, "test": test}

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


def generate(size=None, diags=None, color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    diags: a list of diagonals where we use the color
    color: a digit representing a color to be used
  """
  if size is None:
    size = common.randint(3, 15)
    num_diags = common.randint(1, size // 3)
    top_diags = list(range(0, -size + 1, -2))  # Odd tops are ambiguous.
    bottom_diags = list(range(1, size - 1))
    diags = common.sample(top_diags + bottom_diags, num_diags)
    color = common.random_color(exclude=[common.yellow()])

  grid, output = common.grids(size, size)
  for r in range(size):
    for c in range(size):
      grid[r][c] = color if r - c in diags else common.black()
      if r - c in diags: output[r][c] = (common.yellow() if c % 2 else color)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=3, diags=[0], color=2),
      generate(size=8, diags=[-2, 4], color=9),
      generate(size=6, diags=[-2, 3], color=3),
  ]
  test = [
      generate(size=12, diags=[-4, 1, 8], color=6),
  ]
  return {"train": train, "test": test}

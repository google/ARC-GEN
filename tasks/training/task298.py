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


def generate(half=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    half: half of the width or height of the (square) grid
    colors: a list of three colors to choose from
  """
  if colors is None:
    half = common.randint(3, 4)
    colors = common.sample(range(0, 10), 3)  # Includes black!

  size = 2 * half
  grid, output = common.grids(size, size)
  for r in range(half):
    for c in range(half):
      color_idx = min(r, c) % len(colors)
      grid[r][c] = colors[color_idx]
      grid[r][size - 1 - c] = colors[color_idx]
      grid[size - 1 - r][c] = colors[color_idx]
      grid[size - 1 - r][size - 1 - c] = colors[color_idx]
      color_idx = (min(r, c) + len(colors) - 1) % len(colors)
      output[r][c] = colors[color_idx]
      output[r][size - 1 - c] = colors[color_idx]
      output[size - 1 - r][c] = colors[color_idx]
      output[size - 1 - r][size - 1 - c] = colors[color_idx]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(half=3, colors=[3, 2, 0]),
      generate(half=3, colors=[0, 7, 6]),
      generate(half=4, colors=[8, 0, 5]),
  ]
  test = [
      generate(half=3, colors=[9, 0, 1]),
      generate(half=4, colors=[3, 7, 6]),
  ]
  return {"train": train, "test": test}

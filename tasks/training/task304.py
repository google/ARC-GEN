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


def generate(colors=None, size=3):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) grid
  """
  if colors is None:
    color_list = common.random_colors(common.randint(3, 4))
    colors = common.square_with_unique_max_color(size, color_list)

  grid = common.grid(size, size)
  output = common.grid(size * size, size * size)
  mode = max(set(colors), key=colors.count)
  for r in range(size):
    for c in range(size):
      grid[r][c] = colors[r * size + c]
      if colors[r * size + c] != mode: continue
      for dr in range(size):
        for dc in range(size):
          output[r * size + dr][c * size + dc] = colors[dr * size + dc]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[3, 8, 7, 9, 3, 8, 7, 9, 3]),
      generate(colors=[8, 6, 8, 3, 3, 8, 8, 8, 8]),
      generate(colors=[6, 9, 9, 4, 6, 8, 9, 9, 8]),
  ]
  test = [
      generate(colors=[1, 1, 7, 7, 4, 1, 5, 1, 7]),
  ]
  return {"train": train, "test": test}

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
    color_list = common.random_colors(
        common.randint(2, 4), exclude=[common.gray()]
    )
    colors = common.square_with_unique_max_color(size, color_list)

  grid, output = common.grids(size, size)
  mode = max(set(colors), key=colors.count)
  for r in range(size):
    for c in range(size):
      color = colors[r * size + c]
      grid[r][c] = color
      output[r][c] = color if color == mode else common.gray()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[2, 2, 2, 2, 1, 8, 2, 8, 8]),
      generate(colors=[1, 1, 1, 8, 1, 3, 8, 2, 2]),
      generate(colors=[2, 2, 2, 8, 8, 2, 2, 2, 2]),
      generate(colors=[3, 3, 8, 4, 4, 4, 8, 1, 1]),
  ]
  test = [
      generate(colors=[1, 3, 2, 3, 3, 2, 1, 3, 2]),
  ]
  return {"train": train, "test": test}

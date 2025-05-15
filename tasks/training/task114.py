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


def generate(width=None, height=None, colors=None, color_list=(1, 2, 3, 4, 8)):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    colors: a list of colors to be used in the input grid
    color_list: the subset of colors that are used for this puzzle
  """
  if width is None:
    width, height = common.randint(2, 3), common.randint(2, 3)
    size = width * height
    idxs = [common.randint(0, len(color_list) - 1) for _ in range(size)]
    colors = [color_list[i] for i in idxs]
    if width == 3 and height == 3:
      colors[4] = common.black()  # middle pixel should be the background color

  grid = common.grid(width, height)
  output = common.grid(width + 2, height + 2)
  for r in range(height):
    for c in range(width):
      color = output[r + 1][c + 1] = grid[r][c] = colors[r * width + c]
      if r == 0:
        output[r][c + 1] = color
      if r + 1 == height:
        output[height + 1][c + 1] = color
      if c == 0:
        output[r + 1][c] = color
      if c + 1 == width:
        output[r + 1][width + 1] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=2, height=2, colors=[1, 2, 3, 8]),
      generate(width=3, height=2, colors=[1, 8, 4, 8, 3, 8]),
      generate(width=3, height=3, colors=[2, 1, 4, 8, 0, 2, 3, 2, 8]),
  ]
  test = [
      generate(width=2, height=3, colors=[2, 8, 1, 4, 3, 4]),
  ]
  return {"train": train, "test": test}

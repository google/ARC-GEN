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


def generate(width=None, height=None, vert=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the output grid
    height: the height of the output grid
    vert: whether to duplicate vertically
    colors: the colors of the pixels to be placed
  """
  if width is None:
    width, height = common.randint(2, 4), common.randint(2, 4)
    color_list = common.random_colors(common.randint(3, 4))
    colors = [common.choice(color_list) for _ in range(width * height)]
    vert = common.randint(0, 1)

  grid = common.grid(width * (1 if vert else 2), height * (2 if vert else 1))
  output = common.grid(width, height)
  dr, dc = height if vert else 0, 0 if vert else width
  for r in range(height):
    for c in range(width):
      output[r][c] = grid[r + dr][c + dc] = grid[r][c] = colors[r * width + c]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=4, height=4, vert=0,
               colors=[1, 1, 3, 2, 1, 1, 3, 3, 3, 3, 1, 1, 2, 3, 1, 1]),
      generate(width=3, height=3, vert=0, colors=[4, 4, 4, 6, 4, 8, 6, 6, 8]),
      generate(width=2, height=3, vert=1, colors=[2, 3, 3, 2, 4, 4]),
  ]
  test = [
      generate(width=3, height=4, vert=1,
               colors=[5, 4, 5, 4, 5, 4, 6, 6, 4, 2, 6, 2]),
  ]
  return {"train": train, "test": test}

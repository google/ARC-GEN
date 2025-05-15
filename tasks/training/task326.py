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


def generate(width=None, height=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    colors: the colors of the input grid
  """
  if width is None:
    size = 2 * common.randint(2, 3)
    width, height = size * common.randint(1, 2), size * common.randint(1, 2)
    color_list = common.sample(range(10), common.randint(3, 4))
    colors = [common.choice(color_list) for _ in range(width * height)]

  grid, output = common.grid(width, height), common.grid(2, 2)
  for r in range(height):
    for c in range(width):
      grid[r][c] = colors[r * width + c]
      if r < 2 and c < 2: output[r][c] = colors[r * width + c]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=6, height=6,
               colors=[4, 3, 6, 4, 0, 6, 6, 0, 0, 3, 3, 4, 6, 4, 4, 3, 3, 0, 0,
                       3, 6, 0, 4, 6, 0, 6, 3, 0, 4, 3, 3, 4, 4, 6, 6, 0]),
      generate(width=8, height=8,
               colors=[2, 4, 2, 2, 5, 2, 4, 5, 2, 5, 5, 4, 4, 2, 2, 2, 4, 5, 5,
                       2, 2, 2, 2, 4, 2, 2, 4, 2, 5, 4, 2, 5, 2, 4, 2, 2, 5, 2,
                       4, 5, 2, 5, 5, 4, 4, 2, 2, 2, 4, 5, 5, 2, 2, 2, 2, 4, 2,
                       2, 4, 2, 5, 4, 2, 5]),
      generate(width=6, height=12,
               colors=[3, 2, 1, 3, 4, 1, 1, 4, 4, 2, 2, 3, 1, 3, 3, 2, 2, 4, 4,
                       2, 1, 4, 3, 1, 4, 1, 2, 4, 3, 2, 2, 3, 3, 1, 1, 4, 2, 4,
                       4, 1, 1, 3, 3, 1, 2, 3, 4, 2, 3, 2, 1, 3, 4, 1, 1, 4, 4,
                       2, 2, 3, 1, 3, 3, 2, 2, 4, 4, 2, 1, 4, 3, 1]),
  ]
  test = [
      generate(width=8, height=4,
               colors=[9, 6, 2, 9, 9, 2, 6, 9, 2, 9, 9, 6, 6, 9, 9, 2, 6, 9, 9,
                       2, 2, 9, 9, 6, 9, 2, 6, 9, 9, 6, 2, 9]),
  ]
  return {"train": train, "test": test}

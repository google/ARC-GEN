# Copyright 2026 Google LLC
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
    width: The width of the grid.
    height: The height of the grid.
    colors: The colors of the pixels.
  """

  if width is None:
    width, height = common.randint(1, 5), common.randint(1, 5)
    first, second = common.sample(range(9), k=2), common.sample(range(9), k=2)
    first = [common.choice(first) for _ in range(width * height)]
    second = [common.choice(second) for _ in range(width * height)]
    colors = first + second

  grid = common.grid(width, 2 * height)
  output = common.grid(width + 1, 2 * height + 1, 9)
  for i, color in enumerate(colors):
    grid[i // width][i % width] = color
    if i // width < height:
      output[i // width][i % width] = color
    else:
      output[i // width + 1][i % width + 1] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=2, height=2, colors=[7, 1, 1, 7, 6, 5, 5, 6]),
      generate(width=1, height=1, colors=[4, 0]),
      generate(width=3, height=3, colors=[2, 2, 2, 2, 8, 8, 2, 2, 2, 8, 7, 7, 8, 8, 7, 8, 7, 7]),
  ]
  test = [
      generate(width=5, height=2, colors=[1, 1, 1, 6, 1, 1, 1, 1, 1, 1, 6, 6, 6, 6, 6, 6, 1, 6, 6, 6]),
  ]
  return {"train": train, "test": test}

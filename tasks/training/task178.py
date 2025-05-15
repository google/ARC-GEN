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

import os

import common


def generate(width=None, colors=None, thicks=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    colors: a list of digits representing the colors to be used
    thicks: a list of integers representing the thickness of each layer
    xpose: whether to transpose the grid
  """
  if width is None:
    width = common.randint(1, 5)
    colors = []
    for _ in range(common.randint(3, 5)):
      color = common.random_color()
      if colors:
        color = common.random_color(exclude=[colors[-1]])
      colors.append(color)
    thicks = [common.randint(1, 3) for _ in range(len(colors))]
    xpose = common.randint(0, 1)

  height = sum(thicks)
  grid, output = common.grid(width, height, 0), common.grid(1, len(colors), 0)
  r = 0
  for color, thick in zip(colors, thicks):
    for _ in range(thick):
      for c in range(width):
        grid[r][c] = color
      r += 1
  for r, color in enumerate(colors):
    output[r][0] = color
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=3, colors=[1, 2, 1], thicks=[1, 1, 1], xpose=0),
      generate(width=3, colors=[3, 4, 6], thicks=[1, 1, 1], xpose=1),
      generate(width=3, colors=[2, 3, 8, 1], thicks=[1, 2, 1, 1], xpose=1),
      generate(width=2, colors=[2, 6, 8], thicks=[1, 1, 2], xpose=0),
      generate(width=4, colors=[4, 2, 8, 3], thicks=[2, 2, 1, 1], xpose=0),
  ]
  test = [
      generate(width=4, colors=[1, 2, 3, 8, 4], thicks=[2, 1, 3, 2, 1],
               xpose=1),
  ]
  return {"train": train, "test": test}

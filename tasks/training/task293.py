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


def generate(width=None, height=None, offsets=None, thicks=None, colors=None,
             flip=0):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    offsets: how far these lines are from the edges
    thicks: the thicknesses of the lines
    colors: the colors of the lines
    flip: whether to flip the lines
  """
  if width is None:
    width, height = common.randint(5, 15), common.randint(5, 15)
    thicks = [common.randint(1, 2) for _ in range(2)]
    offsets = [common.randint(1, width - thicks[0] - 1),
               common.randint(1, height - thicks[1] - 1)]
    colors = common.random_colors(2)
    flip = common.randint(0, 1)

  def draw_vertical(thegrid):
    for r in range(height):
      for c in range(offsets[0], offsets[0] + thicks[0]):
        thegrid[r][c] = colors[0]
  def draw_horizontal(thegrid):
    for c in range(width):
      for r in range(offsets[1], offsets[1] + thicks[1]):
        thegrid[r][c] = colors[1]
  grid, output = common.grids(width, height)
  first = draw_vertical if flip else draw_horizontal
  second = draw_horizontal if flip else draw_vertical
  first(grid)
  second(grid)
  second(output)
  first(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=13, height=13, offsets=[3, 3], thicks=[2, 3],
               colors=[8, 3], flip=0),
      generate(width=9, height=7, offsets=[2, 3], thicks=[2, 1], colors=[6, 1],
               flip=1),
      generate(width=7, height=8, offsets=[2, 3], thicks=[1, 1], colors=[1, 7],
               flip=1),
      generate(width=6, height=8, offsets=[1, 4], thicks=[1, 1], colors=[3, 2],
               flip=0),
  ]
  test = [
      generate(width=6, height=11, offsets=[2, 2], thicks=[2, 2], colors=[4, 5],
               flip=0),
  ]
  return {"train": train, "test": test}

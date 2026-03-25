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


def generate(width=None, height=None, length=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    length: The length of the boxes.
    colors: The colors of the boxes.
  """

  if width is None:
    length = common.randint(1, 4)
    width = common.randint(3 * length + 1, 30)
    height = common.randint(3 * length + 1, 30)
    subset = common.random_colors(4, exclude=[7])
    # Make sure there is exactly one "multiple" color.  Otherwise, it's not
    # clear what to do when two different colors move into the center.
    while True:
      colors = common.choices(subset, 4)
      multiples = [c for c in subset if colors.count(c) > 1]
      if len(multiples) == 1: break

  grid, output = common.grids(width, height, 7)
  common.rect(grid, length, length, 0, 0, colors[0])
  common.rect(grid, length, length, 0, width - length, colors[1])
  common.rect(grid, length, length, height - length, 0, colors[2])
  common.rect(grid, length, length, height - length, width - length, colors[3])
  shift0 = 0 if colors.count(colors[0]) == 1 else length
  shift1 = 0 if colors.count(colors[1]) == 1 else length
  shift2 = 0 if colors.count(colors[2]) == 1 else length
  shift3 = 0 if colors.count(colors[3]) == 1 else length
  common.rect(output, length, length, shift0, shift0, colors[0])
  common.rect(output, length, length, shift1, width - length - shift1, colors[1])
  common.rect(output, length, length, height - length - shift2, shift2, colors[2])
  common.rect(output, length, length, height - length - shift3, width - length - shift3, colors[3])
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=16, height=16, length=1, colors=[2, 2, 2, 2]),
      generate(width=17, height=17, length=4, colors=[8, 8, 9, 1]),
      generate(width=15, height=22, length=3, colors=[9, 2, 9, 9]),
      generate(width=7, height=7, length=2, colors=[5, 5, 9, 5]),
  ]
  test = [
      generate(width=30, height=7, length=2, colors=[6, 1, 1, 3]),
  ]
  return {"train": train, "test": test}

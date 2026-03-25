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


def generate(colors=None, colormap=(0, 5, 6, 4, 3, 1, 2, 7, 9, 8)):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of digits representing different colors
    colormap: a list of "target" colors for each possible color
  """
  if colors is None:
    size = common.randint(3, 3)
    colors = common.random_colors(size, exclude=[common.orange()])

  grid = [[color for _ in colors] for color in colors]
  output = [[colormap[color] for _ in colors] for color in colors]
  grid = [list(row) for row in zip(*grid)]
  output = [list(row) for row in zip(*output)]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[3, 1, 2]),
      generate(colors=[2, 3, 8]),
      generate(colors=[5, 8, 6]),
      generate(colors=[9, 4, 2]),
  ]
  test = [
      generate(colors=[8, 1, 3]),
  ]
  return {"train": train, "test": test}

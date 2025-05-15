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


def generate(colors=None, idxs=None, size=3):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a digit representing a color to be used
    idxs: a list of indices into the colors list
    size: the width and height of the (square) grid
  """
  if colors is None:
    colors = [common.random_color() for _ in range(4)]
    idxs = [common.choice(range(len(colors))) for _ in range(size * size)]

  grid = []
  for r in range(size):
    grid.append([colors[idxs[r * size + c]] for c in range(size)])
  output = []
  for r in range(size):
    output.append(grid[r][:] + grid[r][::-1])
  for r in range(size):
    output.append(grid[size - r - 1][:] + grid[size - r - 1][::-1])
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[5, 3, 4, 4], idxs=[0, 1, 2, 1, 2, 0, 1, 3, 3]),
      generate(colors=[7, 1, 5, 3], idxs=[0, 1, 2, 0, 0, 1, 2, 3, 1]),
      generate(colors=[2, 5, 6, 4], idxs=[0, 1, 0, 0, 2, 3, 0, 0, 0]),
      generate(colors=[1, 2, 8, 6], idxs=[0, 1, 0, 1, 2, 0, 2, 0, 3]),
  ]
  test = [
      generate(colors=[1, 6, 5, 2], idxs=[0, 1, 1, 2, 3, 3, 3, 3, 3]),
  ]
  return {"train": train, "test": test}

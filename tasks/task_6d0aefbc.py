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


def generate(idxs=None, size=3, colors=(1, 6, 8)):
  """Returns input and output grids according to the given parameters.

  Args:
    idxs: a list of indices into the colors list
    size: the width and height of the (square) grid
    colors: the colors to use
  """
  if idxs is None:
    idxs = [common.randint(0, len(colors) - 1) for _ in range(size * size)]

  grid, output = common.grid(size, size, 0), common.grid(2 * size, size, 0)
  for r in range(size):
    for c in range(size):
      color = colors[idxs[r * size + c]]
      output[r][2 * size - c - 1] = output[r][c] = grid[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(idxs=[1, 1, 1, 0, 1, 0, 2, 2, 1]),
      generate(idxs=[1, 2, 0, 1, 0, 0, 0, 0, 1]),
      generate(idxs=[0, 0, 0, 2, 0, 1, 1, 2, 2]),
      generate(idxs=[0, 0, 0, 0, 1, 1, 1, 1, 1]),
  ]
  test = [
      generate(idxs=[1, 2, 1, 2, 1, 2, 0, 1, 0]),
  ]
  return {"train": train, "test": test}

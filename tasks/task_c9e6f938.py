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


def generate(rows=None, cols=None, size=3):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    size: the width and height of the (square) grid
  """
  if rows is None:
    while True:
      pixels = common.random_pixels(size, size)
      if pixels: break
    rows, cols = zip(*pixels)

  grid, output = common.grid(size, size), common.grid(2 * size, size)
  for r, c in zip(rows, cols):
    output[r][2 * size - 1 - c] = output[r][c] = grid[r][c] = common.orange()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1, 2, 2], cols=[1, 2, 1, 2]),
      generate(rows=[1, 1], cols=[1, 2]),
      generate(rows=[1], cols=[0]),
  ]
  test = [
      generate(rows=[0, 0, 1, 2], cols=[0, 1, 1, 2]),
  ]
  return {"train": train, "test": test}

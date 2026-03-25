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


def generate(length=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    length: The length to match.
    colors: The colors to use.
  """

  def draw():
    grid, output = common.grids(10, 10)
    for c in range(length):
      output[0][c] = grid[0][c] = 8
    matches = False
    for c, color in enumerate(colors):
      output[8][c] = grid[8][c] = color
      output[6][c] = grid[6][c] = 5
      if colors.count(color) != length: continue
      matches = True
      for r in range(length):
        output[5 - r][c] = color
    if not matches: return None, None
    return grid, output

  if length is None:
    length = common.randint(1, 5)
    subset = common.sample([1, 2, 3, 4, 6, 7, 8, 9], common.randint(2, 5))
    while True:
      colors = common.choices(subset, 10)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(length=2, colors=[2, 3, 3, 2, 3, 1, 1, 3, 1, 1]),
      generate(length=1, colors=[6, 6, 4, 6, 2, 1, 9, 2, 9, 4]),
      generate(length=3, colors=[4, 1, 4, 4, 6, 3, 1, 6, 3, 6]),
      generate(length=4, colors=[2, 1, 2, 1, 2, 1, 1, 2, 2, 2]),
      generate(length=3, colors=[8, 6, 4, 3, 4, 7, 3, 8, 3, 7]),
      generate(length=1, colors=[1, 3, 1, 1, 1, 1, 4, 1, 1, 1]),
  ]
  test = [
      generate(length=2, colors=[2, 3, 6, 4, 6, 2, 4, 4, 3, 9]),
  ]
  return {"train": train, "test": test}

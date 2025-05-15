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


def generate(cols=None, colors=(2, 4, 3), size=3):
  """Returns input and output grids according to the given parameters.

  Args:
    cols: a list of horizontal coordinates where pixels should be placed
    colors: digit representing colors to be used
    size: the width and height of the (square) grid
  """
  if cols is None:
    cols = common.shuffle(range(size))

  grid, output = common.grids(size, size)
  for r, col in enumerate(cols):
    grid[r][col] = common.gray()
    for c in range(size):
      output[r][c] = colors[col]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(cols=[2, 1, 0]),
      generate(cols=[2, 2, 2]),
      generate(cols=[0, 1, 0]),
      generate(cols=[1, 2, 1]),
  ]
  test = [
      generate(cols=[2, 0, 1]),
  ]
  return {"train": train, "test": test}

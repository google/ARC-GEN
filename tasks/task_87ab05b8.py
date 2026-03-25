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


def generate(colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: The colors of the pixels.
  """

  if colors is None:
    colors = [6] * 16
    for _ in range(7):
      colors[common.randint(0, 15)] = common.choice([0, 1, 3, 4, 5, 6, 7, 8, 9])
    colors[common.randint(0, 15)] = 2

  grid, output = common.grids(4, 4, 6)
  for i, color in enumerate(colors):
    row, col = i // 4, i % 4
    grid[row][col] = color
    if color != 2: continue
    r, c = 0 if row < 2 else 2, 0 if col < 2 else 2
    output[r][c] = output[r][c + 1] = output[r + 1][c] = output[r + 1][c + 1] = 2
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[6, 6, 6, 6, 6, 9, 6, 1, 4, 6, 6, 2, 6, 6, 5, 6]),
      generate(colors=[5, 6, 0, 6, 6, 6, 6, 6, 6, 2, 6, 6, 6, 6, 6, 4]),
      generate(colors=[6, 9, 0, 0, 9, 6, 1, 6, 6, 6, 6, 1, 8, 6, 6, 2]),
  ]
  test = [
      generate(colors=[2, 6, 8, 1, 6, 6, 6, 6, 4, 6, 9, 9, 0, 5, 6, 6]),
  ]
  return {"train": train, "test": test}

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


def generate(copies=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    copies: The number of copies.
    colors: The colors of the boxes.
  """

  if copies is None:
    copies = common.randint(3, 4)
    colors = [common.random_color() for _ in range(4)]

  width = 14 if copies == 3 else 30
  height = 10 if copies == 3 else 16
  grid, output = common.grids(width, height)
  row, col = 4 if copies == 3 else 7, 0
  for i in range(copies):
    if not i:
      common.rect(grid, pow(2, i), pow(2, i), row - pow(2, i) + 1, col, colors[0])
      common.rect(grid, pow(2, i), pow(2, i), row - pow(2, i) + 1, col + pow(2, i), colors[1])
      common.rect(grid, pow(2, i), pow(2, i), row + 1, col, colors[2])
      common.rect(grid, pow(2, i), pow(2, i), row + 1, col + pow(2, i), colors[3])
    common.rect(output, pow(2, i), pow(2, i), row - pow(2, i) + 1, col, colors[0])
    common.rect(output, pow(2, i), pow(2, i), row - pow(2, i) + 1, col + pow(2, i), colors[1])
    common.rect(output, pow(2, i), pow(2, i), row + 1, col, colors[2])
    common.rect(output, pow(2, i), pow(2, i), row + 1, col + pow(2, i), colors[3])
    col += pow(2, i + 1)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(copies=3, colors=[2, 5, 5, 3]),
      generate(copies=3, colors=[2, 3, 1, 1]),
      generate(copies=4, colors=[1, 2, 3, 4]),
  ]
  test = [
      generate(copies=4, colors=[1, 1, 8, 8]),
  ]
  return {"train": train, "test": test}

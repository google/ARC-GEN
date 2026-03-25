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


def generate(sizes=None, brows=None, bcols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    sizes: The sizes of the outer box and inner box.
    brows: The rows of the outer box and inner box.
    bcols: The columns of the outer box and inner box.
    colors: A list of colors to use.
  """

  if sizes is None:
    base = common.randint(3, 5)
    sizes = [2 * base, 2 * common.randint(1, base - 2)]
    brows = [common.randint(0, 14 - sizes[0])]
    bcols = [common.randint(0, 14 - sizes[0])]
    brows.append(common.randint(0, sizes[0] - sizes[1] - 2))
    bcols.append(common.randint(0, sizes[0] - sizes[1] - 2))
    colors = common.random_colors(4, exclude=[2])

  grid = common.grid(14, 14)
  output = common.grid(sizes[0], sizes[0])
  common.hollow_rect(grid, sizes[0], sizes[0], brows[0], bcols[0], 2)
  common.hollow_rect(output, sizes[0], sizes[0], 0, 0, 2)
  in_length, out_length = sizes[1] // 2, (sizes[0] - 2) // 2
  for row in range(2):
    for col in range(2):
      r = brows[0] + 1 + brows[1] + row * in_length
      c = bcols[0] + 1 + bcols[1] + col * in_length
      common.rect(grid, in_length, in_length, r, c, colors[row * 2 + col])
      r = 1 + row * out_length
      c = 1 + col * out_length
      common.rect(output, out_length, out_length, r, c, colors[row * 2 + col])
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(sizes=[6, 2], brows=[1, 0], bcols=[4, 1], colors=[3, 5, 6, 8]),
      generate(sizes=[10, 4], brows=[1, 1], bcols=[2, 1], colors=[3, 4, 1, 8]),
  ]
  test = [
      generate(sizes=[10, 4], brows=[4, 0], bcols=[1, 1], colors=[3, 6, 4, 1]),
  ]
  return {"train": train, "test": test}

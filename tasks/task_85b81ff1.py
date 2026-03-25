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


def generate(vals=None, color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    vals: The values of the columns.
    color: The color of the grids.
  """

  width, height = 5, 6
  if vals is None:
    in_order = {}
    counts = common.sample(range(1, height + 1), k=width)
    for count in counts:
      idxs = common.sample(range(height), k=count)
      in_order[count] = [1 if i in idxs else 0 for i in range(height)]
    vals = []
    for order in common.shuffle(list(in_order.keys())):
      vals.extend(in_order[order])
    color = common.random_color()

  grid, output = common.grids(3 * width - 1, 2 * height + 1, color)
  for i in range(width - 1):
    for r in range(2 * height + 1):
      output[r][3 * i + 2] = grid[r][3 * i + 2] = 0
  for i, val in enumerate(vals):
    grid[2 * (i % height) + 1][3 * (i // height) + 1] = 0 if val else color
  in_order = {}
  for i in range(width):
    column = vals[height * i:height * (i + 1)]
    count = sum(column)
    in_order[count] = column
  for col, count in enumerate(sorted(in_order.keys(), reverse=True)):
    for r in range(height):
      output[2 * r + 1][3 * col + 1] = 0 if in_order[count][r] else color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(vals=[1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0], color=1),
      generate(vals=[0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1], color=7),
      generate(vals=[1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1], color=1),
      generate(vals=[1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1], color=6),
  ]
  test = [
      generate(vals=[1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0], color=6),
  ]
  return {"train": train, "test": test}

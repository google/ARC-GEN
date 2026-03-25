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


def generate(colors=None, size=3):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) grid
  """
  if colors is None:
    # Take 3 or 4 random colors
    color_list = common.random_colors(common.randint(3, 4),
                                      exclude=[common.gray()])
    # Create the solid rows first
    rows = []
    for i in range(common.randint(1, 2)):
      rows.append([color_list[i]] * size)
    # Create the other rows, where each has two different (shuffled) colors
    while len(rows) < size:
      idxs = common.sample(color_list, 2)
      rows.append(common.shuffle([idxs[0], idxs[0], idxs[1]]))
    # Shuffle the rows and combine them into a single flat list
    rows = common.shuffle(rows)
    colors = []
    for row in rows:
      colors.extend(row)

  grid, output = common.grids(size, size)
  for r in range(size):
    row = colors[r * size:(r + 1) * size]
    grid[r] = row
    output[r] = [common.gray() if len(set(row)) == 1 else common.black()] * size

  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[4, 4, 4, 2, 3, 2, 2, 3, 3]),
      generate(colors=[7, 3, 3, 6, 6, 6, 3, 7, 7]),
      generate(colors=[2, 9, 2, 4, 4, 4, 9, 9, 9]),
      generate(colors=[2, 2, 4, 2, 2, 4, 1, 1, 1]),
  ]
  test = [
      generate(colors=[4, 4, 4, 3, 2, 3, 8, 8, 8]),
  ]
  return {"train": train, "test": test}

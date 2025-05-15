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


def generate(
    width=None,
    height=None,
    rows=None,
    cols=None,
    colors=None,
    tworows=None,
    twocols=None,
):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing colors to be used
    tworows: a list of vertical coordinates where the two sprites should live
    twocols: a list of horizontal coordinates where the two sprites should live
  """
  if width is None:
    width, height = common.randint(7, 12), common.randint(7, 12)
    while True:
      rows, cols = common.conway_sprite()
      if (1, 1) not in zip(rows, cols): continue  # Center must be taken.
      if common.connected(list(zip(rows, cols))): break
    color_list = common.sample([1, 2, 3, 6], 3)
    colors = [color_list[common.randint(0, 2)] for _ in range(len(rows))]
    while True:
      tworows = common.sample(range(1, height - 1), 2)
      twocols = common.sample(range(1, width - 1), 2)
      if abs(tworows[1] - tworows[0]) >= 4: break
      if abs(twocols[1] - twocols[0]) >= 4: break

  grid, output = common.grids(width, height)
  for idx in range(2):
    if idx:
      grid[tworows[idx]][twocols[idx]] = common.gray()
    for r, c, color in zip(rows, cols, colors):
      output[tworows[idx] + r - 1][twocols[idx] + c - 1] = color
      if idx == 0:
        grid[tworows[idx] + r - 1][twocols[idx] + c - 1] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=9, height=9, rows=[0, 1, 1, 1, 2, 2],
               cols=[1, 0, 1, 2, 1, 2], colors=[2, 2, 2, 1, 1, 3],
               tworows=[1, 5], twocols=[1, 5]),
      generate(width=7, height=8, rows=[0, 1, 1, 2, 2, 2],
               cols=[0, 0, 1, 0, 1, 2], colors=[6, 1, 1, 2, 2, 2],
               tworows=[1, 5], twocols=[5, 1]),
      generate(width=8, height=10, rows=[0, 0, 1, 1, 2, 2, 2],
               cols=[0, 1, 1, 2, 0, 1, 2], colors=[2, 2, 3, 1, 3, 3, 1],
               tworows=[7, 2], twocols=[2, 4]),
  ]
  test = [
      generate(width=11, height=10, rows=[0, 0, 1, 1, 2, 2],
               cols=[1, 2, 0, 1, 1, 2], colors=[2, 2, 1, 1, 3, 3],
               tworows=[3, 8], twocols=[3, 6]),
  ]
  return {"train": train, "test": test}

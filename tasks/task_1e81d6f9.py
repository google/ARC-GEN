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


def generate(target=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    target: The target color.
    colors: The colors to use for the grid.
  """

  if target is None:
    target = common.random_color(exclude=[5])
    while True:
      colors = [0] * (15 * 15)
      for i in range(len(colors)):
        if common.randint(0, 9) == 0: colors[i] = common.random_color()
      if target in colors: break

  grid, output = common.grids(15, 15)
  for i, color in enumerate(colors):
    grid[i // 15][i % 15] = color
    output[i // 15][i % 15] = color if color != target else 0
  for g in [grid, output]:
    common.rect(g, 5, 5, -1, -1, 5)
    common.rect(g, 3, 3, 0, 0, 0)
    g[1][1] = target
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(target=4, colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 9, 2, 4, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 4, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
                                 0, 0, 3, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2,
                                 0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 4, 0, 0, 0, 0,
                                 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2,
                                 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 3, 2, 0, 0, 0, 0, 2, 0, 0, 1, 0, 0,
                                 0, 0, 3, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0,
                                 0, 0, 0, 0, 0, 3, 0, 7, 8, 0, 0, 0, 0, 0, 0]),
      generate(target=2, colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2,
                                 0, 0, 0, 0, 0, 0, 0, 8, 0, 7, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 9, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 7, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2,
                                 0, 0, 6, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 4, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0]),
      generate(target=3, colors=[0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3,
                                 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 9, 0, 0, 0, 9,
                                 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 4,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0,
                                 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 4, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 9, 0, 1,
                                 4, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 4,
                                 0, 8, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 9, 0, 0, 0, 0, 5, 0, 0, 0, 0, 2, 0, 0, 0,
                                 0, 0, 0, 0, 0, 4, 0, 0, 0, 3, 0, 0, 0, 0, 9,
                                 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 3, 0, 0, 0, 1, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 3, 0, 0, 6, 0, 0, 1, 0, 0, 8]),
  ]
  test = [
      generate(target=1, colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 8, 0, 0, 0, 7,
                                 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 6, 2, 0,
                                 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 3, 0, 0, 0, 0,
                                 0, 0, 0, 1, 0, 8, 7, 0, 0, 0, 0, 0, 0, 3, 0,
                                 0, 0, 0, 0, 7, 0, 0, 7, 2, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 4, 1, 0, 0, 0, 6, 6, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 2, 0,
                                 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0]),
  ]
  return {"train": train, "test": test}

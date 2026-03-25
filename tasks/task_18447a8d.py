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


def generate(lefts=None, rights=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    lefts: Lengths of the left lines.
    rights: Lengths of the right lines.
    colors: The colors of the groups.
  """

  def get_values(i):
    values = []
    for j in range(len(colors)):
      lengths = []
      for k in range(3):
        lengths.append(lefts[3 * i + k] + rights[3 * j + k])
      if list(set(lengths)) == [5]: values.append(j)
    return values

  def draw():
    grid, output = common.grids(11, 4 * len(colors) + 1, 7)
    for i, color in enumerate(colors):
      values = get_values(i)
      if len(values) != 1: return None, None
      common.rect(output, 5, 3, 4 * i + 1, 0, colors[values[0]])
      for j in range(3):
        for k in range(rights[3 * i + j]):
          grid[4 * i + j + 1][10 - k] = color
        for k in range(lefts[3 * i + j]):
          output[4 * i + j + 1][k] = grid[4 * i + j + 1][k] = 8
    return grid, output

  if lefts is None:
    colors = common.random_colors(common.randint(3, 4), exclude=[7, 8])
    while True:
      lefts, rights = [], []
      for _ in colors:
        left, right = [], []
        for _ in range(3):
          value = common.randint(1, 4)
          left, right = left + [value], right + [5 - value]
        lefts, rights = lefts + [left], rights + [right]
      lefts = common.flatten(lefts)
      rights = common.flatten(common.shuffle(rights))
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(lefts=[2, 2, 2, 1, 3, 1, 3, 1, 3],
               rights=[4, 2, 4, 2, 4, 2, 3, 3, 3], colors=[9, 3, 1]),
      generate(lefts=[3, 1, 2, 3, 2, 1], rights=[2, 4, 3, 2, 3, 4],
               colors=[9, 2]),
      generate(lefts=[1, 1, 2, 2, 3, 2, 1, 4, 3, 1, 3, 4],
               rights=[4, 4, 3, 4, 2, 1, 3, 2, 3, 4, 1, 2],
               colors=[2, 4, 3, 6]),
  ]
  test = [
      generate(lefts=[2, 4, 1, 2, 3, 1, 3, 4, 1, 3, 4, 2],
               rights=[2, 1, 4, 2, 1, 3, 3, 1, 4, 3, 2, 4],
               colors=[1, 2, 9, 5]),
  ]
  return {"train": train, "test": test}

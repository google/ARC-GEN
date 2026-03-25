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
    while True:
      colors = [6, 5, 5, 5, 5, 5, 5] * 6
      for _ in range(10):
        length = common.randint(2, 4)
        row = common.randint(0, 6 - length)
        col = common.randint(0, 5)
        cdir = common.randint(0, 1)
        color = common.choice([1, 3, 4, 8, 9])
        for i in range(length):
          if cdir: colors[(row + i) * 7 + col + 1] = color
          else: colors[col * 7 + row + i + 1] = color
      colors[common.randint(0, 5) * 7] = 2
      if len(set(colors)) == 7: break

  grid, output = common.grid(7, 6), common.grid(6, 6)
  offset = [r for r in range(6) if colors[7 * r] == 2][0]
  for i, color in enumerate(colors):
    grid[i // 7][i % 7] = color
    if i % 7: output[(i // 7 + offset) % 6][i % 7 - 1] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[2, 1, 1, 1, 1, 9, 8,
                       6, 4, 3, 9, 9, 9, 8,
                       6, 4, 3, 9, 3, 8, 8,
                       6, 4, 3, 3, 3, 8, 8,
                       6, 4, 8, 8, 5, 5, 5,
                       6, 4, 5, 5, 5, 3, 3]),
      generate(colors=[6, 8, 8, 8, 4, 4, 4,
                       6, 9, 9, 8, 3, 4, 4,
                       2, 9, 9, 8, 3, 3, 3,
                       6, 9, 1, 1, 1, 5, 3,
                       6, 4, 4, 1, 5, 5, 5,
                       6, 4, 4, 1, 5, 5, 5]),
      generate(colors=[6, 8, 8, 8, 4, 4, 4,
                       6, 8, 9, 8, 4, 9, 1,
                       6, 8, 9, 9, 9, 9, 1,
                       2, 5, 5, 3, 3, 3, 1,
                       6, 5, 5, 3, 4, 3, 1,
                       6, 5, 5, 3, 4, 4, 4]),
  ]
  test = [
      generate(colors=[6, 5, 8, 8, 8, 9, 9,
                       2, 5, 4, 4, 4, 4, 9,
                       6, 5, 3, 1, 1, 4, 9,
                       6, 5, 3, 1, 1, 4, 8,
                       6, 1, 3, 3, 3, 8, 8,
                       6, 1, 1, 3, 8, 8, 9]),
  ]
  return {"train": train, "test": test}

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


def generate(colors=None, pattern=None, shown=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
    pattern: The bitmap pattern.
    shown: A list of shown pixel indices.
  """

  if colors is None:
    while True:
      colors = []
      for _ in range(4):
        colors.extend(common.sample(list(range(0, 10)), 2))
      if len(set(colors)) >= 7: break  # We want them mostly different.
    while True:
      pattern = [common.randint(0, 1) for _ in range(16)]
      if sum(pattern) >= 6 and sum(pattern) <= 10: break
    shown = []
    for _ in range(3):
      while True:
        pair = common.sample(list(range(16)), 2)
        if pattern[pair[0]] != pattern[pair[1]]: break
      shown.extend(pair)
    pattern = "".join(str(p) for p in pattern)

  grid, output = common.grids(10, 10)
  for i, char in enumerate(pattern):
    p = int(char)
    grid[i // 4 + 1][i % 4 + 1] = colors[p + 0]
    if i in shown[0:2]: grid[i // 4 + 1][8 - i % 4] = colors[p + 2]
    if i in shown[2:4]: grid[8 - i // 4][i % 4 + 1] = colors[p + 4]
    if i in shown[4:6]: grid[8 - i // 4][8 - i % 4] = colors[p + 6]
    output[i // 4 + 1][i % 4 + 1] = colors[p + 0]
    output[i // 4 + 1][8 - i % 4] = colors[p + 2]
    output[8 - i // 4][i % 4 + 1] = colors[p + 4]
    output[8 - i // 4][8 - i % 4] = colors[p + 6]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[3, 8, 9, 7, 4, 1, 2, 5], pattern="0000001101010110",
               shown=[3, 7, 11, 15, 10, 11]),
      generate(colors=[2, 1, 8, 3, 4, 7, 5, 0], pattern="0101110100011111",
               shown=[0, 15, 0, 15, 0, 15]),
      generate(colors=[8, 2, 1, 6, 4, 5, 3, 1], pattern="0100111101000100",
               shown=[7, 14, 13, 14, 5, 15]),
  ]
  test = [
      generate(colors=[4, 1, 5, 8, 6, 7, 0, 3], pattern="0011011111101100",
               shown=[3, 15, 8, 14, 10, 15]),
  ]
  return {"train": train, "test": test}

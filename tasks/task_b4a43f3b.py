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


def generate(colors=None, pattern=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
    pattern: A list of patterns to use.
  """

  if colors is None:
    sprite = common.diagonally_connected_sprite(3, 3)
    colors = ""
    for r in range(3):
      for c in range(3):
        colors += str(common.choice([1, 2, 3, 6]) if (r, c) in sprite else 0)
    grid = common.grid(6, 6)
    for _ in range(3):
      length = common.randint(1, 6)
      pos = common.randint(0, 6 - length)
      val = common.randint(0, 5)
      cdir = common.randint(0, 1)
      for i in range(pos, pos + length):
        grid[val if cdir else i][i if cdir else val] = 2
    pattern = "".join(str(x) for x in common.flatten(grid))

  grid, output = common.grid(6, 13), common.grid(18, 18)
  for c in range(6):
    grid[6][c] = 5
  for row in range(3):
    for col in range(3):
      common.rect(grid, 2, 2, row * 2, col * 2, int(colors[row * 3 + col]))
  for row in range(6):
    for col in range(6):
      if pattern[row * 6 + col] == "0": continue
      grid[row + 7][col] = 2
      for r in range(3):
        for c in range(3):
          output[row * 3 + r][col * 3 + c] = int(colors[r * 3 + c])
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors="101020320",
               pattern="000000002000022220002000000000000000"),
      generate(colors="136010221",
               pattern="000000220000220000002000000200000000"),
      generate(colors="101010333",
               pattern="000000000000002000002000022200000000"),
      generate(colors="320020061",
               pattern="000000020000002000022220000000000000"),
  ]
  test = [
      generate(colors="010303020",
               pattern="202000002000222222002000002000002000"),
  ]
  return {"train": train, "test": test}

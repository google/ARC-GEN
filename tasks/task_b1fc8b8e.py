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
    colors: A list of colors to use.
  """

  if colors is None:
    shape = common.randint(0, 1)
    while True:
      colors = [0] * 36
      rows = [common.randint(0, 4) for _ in range(4)]
      cols = [common.randint(0, 4) for _ in range(4)]
      good = True  # First, check that no overlap
      for row, col  in zip(rows, cols):
        for r, c in [(0, 0), (0, 1), (1, 0), (1, 1)]:
          if shape == 0 and r == 0 and c == 0: continue
          if colors[(row + r) * 6 + col + c]: good = False
          colors[(row + r) * 6 + col + c] = 1
      if not good: continue
      if shape == 0:
        good = False  # If shape is 0, check that there's some "nesting."
        for row, col in zip(rows, cols):
          if colors[row * 6 + col]: good = True
      if good: break
    colors = "".join(map(str, colors))

  grid, output = common.grid(6, 6), common.grid(5, 5)
  for i, color in enumerate(colors):
    grid[i // 6][i % 6] = 8 * int(color)
  for r in range(5):
    for c in range(5):
      if r % 3 == 2 or c % 3 == 2: continue
      if r % 3 == 0 and c % 3 == 0 and colors.count("1") == 12: continue
      output[r][c] = 8
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors="111100111111011011011000000000000000"),
      generate(colors="001100111100111111001111000000000000"),
      generate(colors="000100011100111010011110000000000000"),
      generate(colors="000100011110111110011000000000000000"),
      generate(colors="000100001110010110111000011000000000"),
  ]
  test = [
      generate(colors="010100111110000111000011000000000000"),
      generate(colors="001100111100110110011110011000000000"),
  ]
  return {"train": train, "test": test}

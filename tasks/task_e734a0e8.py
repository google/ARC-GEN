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


def generate(minisize=None, megasize=None, pattern="", dots=""):
  """Returns input and output grids according to the given parameters.

  Args:
    minisize: The size of the mini square.
    megasize: The number of mini squares per side.
    pattern: The pattern of the mini square.
    dots: The pattern of the dots.
  """

  if minisize is None:
    megasize = 3 if common.randint(0, 1) else 4
    minisize = 3 if common.randint(0, 1) else 5
    while True:
      dots = [common.randint(0, 1) for _ in range(megasize * megasize)]
      dots[common.randint(0, len(dots) - 1)] = 2
      if len(set(dots)) == 3: break
    color = common.random_color(exclude=[7])
    while True:
      pixels = []
      for row in range(minisize):
        for col in range(minisize):
          if common.randint(0, 2) == 0: pixels.append((row, col))
      if pixels and common.diagonally_connected(pixels): break
    pattern = []
    for row in range(minisize):
      for col in range(minisize):
        pattern.append(color if (row, col) in pixels else 7)
    dots = "".join(map(str, dots))
    pattern = "".join(map(str, pattern))

  size = (minisize + 1) * megasize - 1
  grid, output = common.grids(size, size)
  for megarow in range(megasize):
    for megacol in range(megasize):
      common.rect(grid, minisize, minisize, megarow * (minisize + 1),
                  megacol * (minisize + 1), 7)
      common.rect(output, minisize, minisize, megarow * (minisize + 1),
                  megacol * (minisize + 1), 7)
      dot = int(dots[megarow * megasize + megacol])
      if dot == 0: continue
      if dot == 1:
        row = megarow * (minisize + 1) + minisize // 2
        col = megacol * (minisize + 1) + minisize // 2
        grid[row][col] = 0
      for row in range(minisize):
        for col in range(minisize):
          r = megarow * (minisize + 1) + row
          c = megacol * (minisize + 1) + col
          color = int(pattern[row * minisize + col])
          if dot == 2: grid[r][c] = color
          output[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(minisize=5, megasize=4, pattern="7779977797777977999779777",
               dots="0100010000211001"),
      generate(minisize=3, megasize=3, pattern="727727727", dots="200010011"),
  ]
  test = [
      generate(minisize=5, megasize=3, pattern="7747744444774777474747774",
               dots="002010101"),
  ]
  return {"train": train, "test": test}

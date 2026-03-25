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


def generate(grid_color=None, sprite_color=None, colors=None, pattern=None,
             brow=None, bcol=None):
  """Returns input and output grids according to the given parameters.

  Args:
    grid_color: The color of the grid lines.
    sprite_color: The color of the input sprite.
    colors: The colors of the output sprites.
    pattern: The pattern of the sprites.
    brow: The row of the sprite.
    bcol: The column of the sprite.
  """

  if grid_color is None:
    length = common.randint(2, 5)
    grid_color = common.random_color()
    sprite_color = common.random_color(exclude=[grid_color])
    colors = common.random_colors(length, exclude=[grid_color, sprite_color])
    while True:
      pattern = [common.randint(0, 1) for _ in range(16)]
      if sum(pattern) < 6 or sum(pattern) > 10: continue
      pixels = [(i // 4, i % 4) for i, val in enumerate(pattern) if val]
      if common.diagonally_connected(pixels): break
    pattern = "".join(map(str, pattern))
    brow, bcol = common.randint(0, length - 1), common.randint(1, length - 1)

  size = 5 * len(colors) - 1
  grid, output = common.grids(size, size)
  for i in range(4, size, 5):
    for j in range(size):
      output[i][j] = output[j][i] = grid[i][j] = grid[j][i] = grid_color
  for i, color in enumerate(colors):
    common.rect(grid, 2, 2, 5 * i + 1, 1, color)
  for i, val in enumerate(pattern):
    if val == "0": continue
    grid[brow * 5 + i // 4][bcol * 5 + i % 4] = sprite_color
    for row in range(len(colors)):
      for col in range(len(colors)):
        output[row * 5 + i // 4][col * 5 + i % 4] = colors[row]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(grid_color=3, sprite_color=6, colors=[4, 2, 8, 1],
               pattern="0000110101100010", brow=3, bcol=1),
      generate(grid_color=8, sprite_color=5, colors=[2, 3, 1],
               pattern="0110001011110100", brow=0, bcol=1),
  ]
  test = [
      generate(grid_color=5, sprite_color=1, colors=[2, 3, 4, 6, 7],
               pattern="0010111101100010", brow=1, bcol=2),
  ]
  return {"train": train, "test": test}

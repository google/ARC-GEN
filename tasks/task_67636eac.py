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


def generate(width=None, height=None, brows=None, bcols=None, colors=None,
             sprite=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    brows: The rows of the sprites.
    bcols: The columns of the sprites.
    colors: The colors of the sprite.
    sprite: The sprite to draw.
    xpose: Whether to transpose the grid.
  """

  if width is None:
    width, height = common.randint(10, 20), common.randint(10, 20)
    num_sprites = 2
    if width * height >= 125: num_sprites = 3
    if width * height >= 250: num_sprites = 4
    colors = common.sample([1, 2, 3, 4, 8], num_sprites)
    while True:  # Choose locations that overlap in only one direction.
      brows = [common.randint(0, height - 3) for _ in range(num_sprites)]
      bcols = sorted([common.randint(0, width - 3) for _ in range(num_sprites)])
      if common.overlaps(brows, bcols, [3] * num_sprites, [3] * num_sprites, 1):
        continue
      if common.overlaps_1d(bcols, [3] * num_sprites): continue
      if not common.overlaps_1d(brows, [3] * num_sprites): continue
      break
    while True:  # Choose a diagonally connected & symmetric sprite.
      pixels = common.diagonally_connected_sprite(3, 3, common.randint(2, 5))
      sprite = []
      for r in range(3):
        for c in range(3):
          sprite.append(1 if (r, c) in pixels else 0)
      if common.is_symmetric(sprite): break
    xpose = common.randint(0, 1)

  grid, output = common.grid(width, height), common.grid(3 * len(brows), 3)
  for idx, (brow, bcol, color) in enumerate(zip(brows, bcols, colors)):
    for i, value in enumerate(sprite):
      grid[brow + i // 3][bcol + i % 3] = value * color
      output[i // 3][3 * idx + i % 3] = value * color
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=16, height=10, brows=[2, 3, 4], bcols=[1, 6, 11],
               colors=[3, 1, 8], sprite=[0, 1, 0, 1, 0, 1, 0, 1, 0],
               xpose=True),
      generate(width=17, height=13, brows=[1, 5, 2], bcols=[1, 4, 13],
               colors=[2, 3, 8], sprite=[0, 1, 0, 1, 1, 1, 0, 1, 0],
               xpose=False),
      generate(width=12, height=10, brows=[3, 1], bcols=[1, 6], colors=[2, 1],
               sprite=[1, 0, 1, 0, 1, 0, 1, 0, 1], xpose=True),
  ]
  test = [
      generate(width=18, height=14, brows=[3, 4, 2, 3], bcols=[1, 6, 10, 14],
               colors=[4, 2, 3, 1], sprite=[1, 0, 1, 1, 1, 1, 1, 0, 1],
               xpose=False),
  ]
  return {"train": train, "test": test}

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


def generate(width=None, height=None, xpose=None, brows=None, bcols=None,
             bcolors=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
  """

  if width is None:
    num_sprites = common.randint(2, 3)
    width = 6 * num_sprites + common.randint(0, 2)
    height = common.randint(8, 13)
    brows = [common.randint(1, height - 7) for _ in range(num_sprites)]
    bcols = [common.randint(1, 2) for _ in range(num_sprites)]
    bcolors = common.random_colors(num_sprites, exclude=[6])
    colors = []
    for _ in range(num_sprites):
      pixels = common.connected_sprite(4, 4, 8)
      for r in range(4):
        for c in range(4):
          colors.append(6 if (r, c) in pixels else 0)
    colors = "".join(map(str, colors))
    xpose = common.randint(0, 1)

  grid, output = common.grid(width, height), common.grid(4 * len(bcolors), 4)
  for i in range(len(bcolors)):
    brow, bcol, bcolor = brows[i], bcols[i], bcolors[i]
    grid[brow + 5][6 * i + 1 + bcol] = bcolor
    for r in range(4):
      for c in range(4):
        color = int(colors[i * 16 + r * 4 + c])
        grid[brow + r][6 * i + 1 + c] = color
        output[r][4 * i + c] = bcolor if color else 0
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=14, height=12, xpose=0, brows=[2, 2], bcols=[2, 2],
               bcolors=[3, 2], colors="00060666660006660600060066660060"),
      generate(width=12, height=9, xpose=1, brows=[1, 2], bcols=[1, 1],
               bcolors=[8, 1], colors="06006606066606000060666060666000"),
      generate(width=18, height=12, xpose=0, brows=[1, 4, 2], bcols=[1, 1, 2],
               bcolors=[1, 3, 4],
               colors="060066660660060006006600060066666006666606600066"),
  ]
  test = [
      generate(width=18, height=13, xpose=1, brows=[5, 3, 6], bcols=[1, 1, 2],
               bcolors=[1, 7, 3],
               colors="060066606060006666660606060006006666600666060600"),
  ]
  return {"train": train, "test": test}

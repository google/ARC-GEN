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


def generate(width=None, frames=None, offset=None, flip=None, colors=None,
             pattern=None, extra=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the pattern.
    frames: The number of frames to generate.
    offset: The offset of the pattern.
    flip: Whether to flip the pattern.
    colors: The colors to use for the pattern.
    pattern: The pattern to generate.
    extra: Whether to add an extra row (for an ambiguous case).
  """

  if width is None:
    width = common.randint(4, 5)
    frames = common.randint(3, 4)
    offset = common.randint(1, 3 if frames == 3 else 2)
    flip = common.randint(0, 1)
    bgcolor = common.random_color()
    mgcolor = common.random_color(exclude=[bgcolor])
    fgcolor = common.random_color(exclude=[mgcolor])
    colors = [bgcolor, mgcolor, fgcolor]
    pattern = [1] * (width - 2)
    if width == 4:
      a = common.randint(0, 1)
      pattern.extend([a, a])
    if width == 5:
      a, b = common.randint(0, 1), common.randint(0, 1)
      pattern.extend([a, b, a])

  grid = common.grid((width + 1) * frames + 1, 16, colors[0])
  output = common.grid(width + 2, 16, colors[0])
  for f in range(frames):
    common.rect(grid, width, 14, 1, f * (width + 1) + 1, colors[1])
    for row in range(2):
      for col in range(width - 2):
        if not pattern[row * (width - 2) + col]: continue
        grid[2 + f * offset + row][f * (width + 1) + 2 + col] = colors[2]
  common.rect(output, width, 14, 1, 1, colors[1])
  extra = extra if extra else 0
  for row in range(2):
    for col in range(width - 2):
      if not pattern[row * (width - 2) + col]: continue
      output[2 + frames * offset + row + extra][2 + col] = colors[2]
  if flip: grid, output = common.flip(grid), common.flip(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=4, frames=4, offset=1, flip=0, colors=[1, 2, 3],
               pattern=[1, 1, 0, 0]),
      generate(width=4, frames=3, offset=3, flip=0, colors=[8, 2, 8],
               pattern=[1, 1, 1, 1], extra=1),
      generate(width=5, frames=3, offset=3, flip=1, colors=[3, 1, 2],
               pattern=[1, 1, 1, 1, 0, 1]),
  ]
  test = [
      generate(width=5, frames=4, offset=2, flip=0, colors=[4, 3, 8],
               pattern=[1, 1, 1, 0, 1, 0]),
  ]
  return {"train": train, "test": test}

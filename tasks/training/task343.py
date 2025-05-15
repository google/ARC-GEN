# Copyright 2025 Google LLC
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


def generate(lengths=None, colors=None, visible=None, flip=None, width=15,
             height=5):
  """Returns input and output grids according to the given parameters.

  Args:
    lengths: a list of integers representing the lengths of the lines
    colors: a list of digits representing the colors to be used
    visible: the number of columns that should be visible in the input
    flip: whether to flip every other pattern
    width: the width of the input grid
    height: the height of the input grid
  """

  def draw(grid, output):
    flip_iter = 0
    for coloffset in range(0, width, len(lengths)):
      idx = -1
      for dc, length in enumerate(lengths):
        for dr in range(length):
          r, c, idx = height - dr - 1, coloffset + dc, idx + 1
          if flip and flip_iter % 2: c = coloffset + len(lengths) - dc - 1
          if c < visible: common.draw(grid, r, c, colors[idx])
          common.draw(output, r, c, colors[idx])
      flip_iter += 1
    return grid != output

  if lengths is None:
    while True:
      lengths = [common.randint(1, 3) for _ in range(common.randint(3, 4))]
      color_list = common.random_colors(common.randint(2, 3))
      colors = [common.choice(color_list) for _ in range(sum(lengths))]
      flip = common.randint(0, 1)
      visible = (flip + 2) * len(lengths) + common.randint(0, len(lengths) - 1)
      grid, output = common.grids(width, height)
      if draw(grid, output): break

  grid, output = common.grids(width, height)
  draw(grid, output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(lengths=[1, 2, 2], colors=[1, 2, 2, 2, 2], visible=7, flip=0),
      generate(lengths=[1, 1, 3, 1], colors=[3, 3, 2, 2, 2, 1], visible=8,
               flip=0),
      generate(lengths=[3, 2, 1], colors=[4, 4, 4, 3, 3, 2], visible=10,
               flip=1),
  ]
  test = [
      generate(lengths=[2, 2, 3, 1], colors=[6, 6, 6, 2, 2, 2, 2, 3],
               visible=10, flip=0),
  ]
  return {"train": train, "test": test}

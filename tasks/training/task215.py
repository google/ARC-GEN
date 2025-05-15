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


def generate(
    width=None,
    height=None,
    rows=None,
    cols=None,
    offset=None,
    color=None,
    flip=None,
):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    offset: the offset of the pattern
    color: a digit representing a color to be used
    flip: whether to flip the pattern
  """
  if rows is None:
    # TODO: make sure the pattern is 3 pixels tall, or at least flips?
    # TODO: Make sure the flat L-tetris piece is possible?
    width, height = common.randint(10, 20), common.randint(10, 20)
    rows, cols = common.conway_sprite(common.randint(2, 3), 3)
    offset = common.randint(3, 4)
    color = common.random_color()
    flip = common.randint(0, 1)

  grid, output = common.grids(width, height)
  wide = max(cols) + 1
  for i in range(0, width, wide):
    for row, col in zip(rows, cols):
      r = offset + (row if not flip or i % 2 == 0 else 2 - row)
      c = col + i
      common.draw(grid, r, c, color)
  for j in range(-6, height, 3):
    for i in range(0, width, wide):
      for row, col in zip(rows, cols):
        r = offset + (row if not flip or i % 2 == 0 else 2 - row) + j
        c = col + i
        common.draw(output, r, c, color)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=19, height=15, rows=[0, 1, 1, 1], cols=[2, 0, 1, 2],
               offset=4, color=8, flip=1),
      generate(width=12, height=10, rows=[0, 1, 1, 2], cols=[0, 0, 1, 0],
               offset=3, color=2, flip=0),
  ]
  test = [
      generate(width=13, height=14, rows=[0, 1, 1, 2, 2], cols=[1, 0, 2, 0, 2],
               offset=3, color=1, flip=0),
  ]
  return {"train": train, "test": test}

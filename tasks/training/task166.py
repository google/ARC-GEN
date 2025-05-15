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


def generate(width=None, height=None, prow=None, pcol=None, lengths=None,
             brow=None, bcol=None, flip=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    prow: the horizontal coordinate of the cyan pixel
    pcol: the vertical coordinate of the cyan pixel
    lengths: a list of lengths of the cyan strips
    brow: the vertical coordinate of the box
    bcol: the horizontal coordinate of the box
    flip: whether to flip the grids horizontally
    xpose: whether to transpose the grids
  """
  if width is None:
    num_lengths, max_length = common.randint(6, 9), common.randint(4, 6)
    width = max_length + common.randint(3, 6)
    height = num_lengths + common.randint(2, 5)
    lengths = [common.randint(1, max_length) for _ in range(num_lengths)]
    prow = common.randint(0, num_lengths - 2)
    pcol = common.randint(0, lengths[prow + 1] - 1)
    brow = common.randint(1, height - num_lengths - 1)
    bcol = common.randint(1, width - max_length - 1)
    flip, xpose = common.randint(0, 1), common.randint(0, 1)

  grid, output = common.grids(width, height)
  for r in range(len(lengths)):
    for c in range(max(lengths)):
      output[brow + r][bcol + c] = common.red()
  for r, length in enumerate(lengths):
    for c in range(length):
      output[brow + r][bcol + c] = grid[brow + r][bcol + c] = common.cyan()
  grid[brow + prow][bcol + pcol] = common.cyan()
  output[brow + prow][bcol + pcol] = common.cyan()
  if flip: grid, output = common.flip_horiz(grid), common.flip_horiz(output)
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=10, height=14, prow=0, pcol=0,
               lengths=[3, 1, 4, 2, 3, 1, 3, 3, 2], brow=2, bcol=1, flip=0,
               xpose=0),
      generate(width=7, height=8, prow=4, pcol=3,
               lengths=[3, 1, 4, 2, 1, 4], brow=1, bcol=1, flip=0, xpose=1),
      generate(width=8, height=9, prow=1, pcol=2,
               lengths=[5, 1, 4, 3, 2, 3], brow=1, bcol=2, flip=1, xpose=0),
  ]
  test = [
      generate(width=9, height=11, prow=4, pcol=4,
               lengths=[6, 3, 4, 2, 1, 5, 2], brow=2, bcol=1, flip=1, xpose=1),
  ]
  return {"train": train, "test": test}

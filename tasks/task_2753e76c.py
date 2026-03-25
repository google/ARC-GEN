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


def generate(brows=None, bcols=None, lengths=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    lengths: The lengths of the boxes.
    colors: The colors of the boxes.
  """

  if brows is None:
    num_colors = common.randint(3, 4)
    subset = common.sample([1, 2, 3, 4, 8], num_colors)
    while True:
      counts = common.sample(list(range(1, 6)), num_colors)
      brows, bcols, lengths, colors = [], [], [], []
      for color, count in zip(subset, counts):
        sizes = common.choices([2, 2, 2, 2, 3, 3, 3, 4, 4, 5], count)
        brows.extend([common.randint(0, 16 - size) for size in sizes])
        bcols.extend([common.randint(0, 16 - size) for size in sizes])
        lengths.extend(sizes)
        colors.extend([color] * count)
      if not common.overlaps(brows, bcols, lengths, lengths, 1): break

  grid = common.grid(16, 16)
  for brow, bcol, length, color in zip(brows, bcols, lengths, colors):
    common.rect(grid, length, length, brow, bcol, color)
  counts = {item: colors.count(item) for item in set(colors)}
  counts = {v: k for k, v in counts.items()}
  width, height = max(counts.keys()), len(counts.values())
  output = common.grid(width, height)
  for r, (count, color) in enumerate(sorted(counts.items(), reverse=True)):
    for c in range(count):
      output[r][width - 1 - c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(brows=[0, 0, 1, 3, 5, 6, 7, 8, 11, 13], bcols=[8, 13, 3, 10, 6, 0, 12, 7, 3, 12], lengths=[2, 2, 3, 3, 2, 4, 4, 3, 2, 2], colors=[4, 2, 2, 2, 3, 8, 2, 3, 8, 3]),
      generate(brows=[0, 2, 7, 7, 11, 12], bcols=[0, 8, 5, 11, 1, 7], lengths=[5, 4, 4, 2, 2, 3], colors=[8, 8, 8, 1, 2, 2]),
      generate(brows=[0, 0, 1, 2, 4, 6, 7, 7, 11, 12, 13], bcols=[8, 11, 1, 4, 13, 7, 0, 11, 4, 0, 9], lengths=[2, 3, 2, 3, 2, 3, 3, 5, 4, 2, 3], colors=[8, 8, 1, 1, 8, 3, 2, 1, 1, 1, 2]),
  ]
  test = [
      generate(brows=[0, 1, 2, 2, 5, 6, 7, 9, 11, 11, 13], bcols=[6, 1, 10, 14, 4, 9, 14, 5, 1, 9, 4], lengths=[2, 3, 2, 2, 3, 2, 2, 3, 2, 4, 2], colors=[8, 3, 3, 8, 4, 4, 3, 4, 3, 3, 4]),
  ]
  return {"train": train, "test": test}

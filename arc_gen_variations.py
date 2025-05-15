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

"""An example of customized variations using ARC-GEN."""

import common
import task_list


if __name__ == "__main__":
  _, generator, _ = task_list.task_list().get(125)
  examples = []
  # Two examples of a "large" variation on Task #125.
  examples.extend([generator(boxes=8, size=28) for _ in range(2)])
  # Two examples of a "large + inverted" variation on Task #125.
  common.set_colors([0, 1, 2, 6, 8, 5, 3, 7, 4, 9])
  examples.extend([generator(boxes=8, size=28) for _ in range(2)])
  print(examples)

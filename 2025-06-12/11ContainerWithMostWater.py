from typing import List

class Solution:
    def maxArea(self, height: List[int], debug: bool = False) -> int:
        """
        Two-pointer approach to find the maximum water container:

        1. Set two pointers at both ends.
        2. Calculate area between them (width * min height).
        3. Update max area if larger.
        4. Move the pointer on the shorter line inward (to seek taller wall).
        5. Repeat until pointers meet.
        """

        def debugPrint(msg):
            if debug:
                print(str(msg))

        leftContaienrSide: int = 0                     # index of the left container wall
        rightContaienrSide: int = len(height) - 1      # index of the right container wall
        maxSize: int = 0                               # stores the maximum area found

        debugPrint(f"Initial leftContaienrSide: {leftContaienrSide}, rightContaienrSide: {rightContaienrSide}")
        while leftContaienrSide < rightContaienrSide:
            # calculate current width and height
            width = rightContaienrSide - leftContaienrSide
            current_height = min(height[leftContaienrSide], height[rightContaienrSide])
            # compute area with current pair of lines
            areaSize = width * current_height
            debugPrint(f"Indices L={leftContaienrSide}, R={rightContaienrSide} -> width={width}, height={current_height}, area={areaSize}")

            # update maxSize if we found a larger area
            if areaSize > maxSize:
                maxSize = areaSize
                debugPrint(f"  New maxSize={maxSize}")

            # move the pointer at the shorter wall inward
            if height[leftContaienrSide] < height[rightContaienrSide]:
                leftContaienrSide += 1  # move left pointer right
                debugPrint(f"  Move left pointer to {leftContaienrSide}")
            else:
                rightContaienrSide -= 1  # move right pointer left
                debugPrint(f"  Move right pointer to {rightContaienrSide}")

        # when pointers meet or cross, we've checked all possible pairs
        return maxSize

if __name__ == "__main__":
    input_heights = [1,8,6,2,5,4,8,3,7]
    sol = Solution()
    print(sol.maxArea(input_heights, debug=True))  # expect 49

# ---------------------------------------------
# How it works (plain English summary at the end):
# (1) Initialize two pointers: leftContaienrSide = 0, rightContaienrSide = len(height) - 1
# (2) Track maxSize = 0 for the largest area.
# (3) While leftContaienrSide < rightContaienrSide:
#     (a) width = rightContaienrSide - leftContaienrSide
#     (b) current_height = min(height[leftContaienrSide], height[rightContaienrSide])
#     (c) areaSize = width * current_height
#     (d) if areaSize > maxSize: update maxSize
#     (e) move the pointer on the shorter wall inward:
#         - if height[leftContaienrSide] < height[rightContaienrSide], increment leftContaienrSide
#         - else, decrement rightContaienrSide
# (4) Loop ends when pointers meet or cross.
# (5) Return maxSize as the maximum container area.
# ---------------------------------------------

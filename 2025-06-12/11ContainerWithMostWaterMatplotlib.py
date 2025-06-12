from typing import List
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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

def plot_container(height: list, left: int, right: int, max_area: int):
    plt.figure(figsize=(10, 6))
    bars = plt.bar(range(len(height)), height, color='skyblue', edgecolor='black')
    bars[left].set_color('orange')
    bars[right].set_color('orange')
    plt.title(f"Container With Most Water (max area = {max_area})")
    plt.xlabel("Index")
    plt.ylabel("Height")
    # Draw the water area
    plt.fill_between([left, right], [height[left], height[right]], color='deepskyblue', alpha=0.3)
    plt.text((left+right)/2, min(height[left], height[right])+0.5, f'Area: {max_area}',
             ha='center', color='blue', fontsize=12)
    plt.show()

def plot_container_with_steps(height: list, left: int, right: int, max_area: int, steps: list):
    plt.figure(figsize=(12, 7))
    bars = plt.bar(range(len(height)), height, color='skyblue', edgecolor='black')
    bars[left].set_color('orange')
    bars[right].set_color('orange')
    plt.title(f"Container With Most Water (max area = {max_area})")
    plt.xlabel("Index")
    plt.ylabel("Height")
    plt.fill_between([left, right], [height[left], height[right]], color='deepskyblue', alpha=0.3)
    plt.text((left+right)/2, min(height[left], height[right])+0.5, f'Area: {max_area}',
             ha='center', color='blue', fontsize=12)
    plt.show()

    # Step-by-step visualization
    for i, (l, r, area) in enumerate(steps):
        plt.figure(figsize=(10, 5))
        bars = plt.bar(range(len(height)), height, color='lightgrey', edgecolor='black')
        bars[l].set_color('orange')
        bars[r].set_color('orange')
        plt.fill_between([l, r], [height[l], height[r]], color='deepskyblue', alpha=0.2)
        plt.title(f"Step {i+1}: L={l}, R={r}, Area={area}")
        plt.xlabel("Index")
        plt.ylabel("Height")
        plt.text((l+r)/2, min(height[l], height[r])+0.5, f'Area: {area}',
                 ha='center', color='blue', fontsize=11)
        plt.tight_layout()
        plt.show()

def animate_container_steps(height: list, steps: list, interval_ms: int = 800, every_nth: int = 1):
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(range(len(height)), height, color='lightgrey', edgecolor='black')
    text = ax.text(0, 0, '', ha='center', color='blue', fontsize=12)
    ax.set_xlabel('Index')
    ax.set_ylabel('Height')
    ax.set_title('Container With Most Water - Step by Step')
    filtered_steps = steps[::every_nth]

    # Always add the final (best) calculation as last frame if not already included
    best = max(steps, key=lambda x: x[2])
    if filtered_steps[-1] != best:
        filtered_steps.append(best)

    def update(frame):
        l, r, area = filtered_steps[frame]
        for i, bar in enumerate(bars):
            bar.set_color('lightgrey')
        bars[l].set_color('orange')
        bars[r].set_color('orange')
        [coll.remove() for coll in ax.collections]
        ax.fill_between([l, r], [height[l], height[r]], color='deepskyblue', alpha=0.2)
        if frame == len(filtered_steps)-1:
            text.set_text(f'FINAL: L={l}, R={r}, Area={area}')
        else:
            text.set_text(f'Step {frame*every_nth+1}: L={l}, R={r}, Area={area}')
        text.set_position(((l+r)/2, min(height[l], height[r])+0.5))
        return bars, text

    ani = animation.FuncAnimation(fig, update, frames=len(filtered_steps), interval=interval_ms, blit=False, repeat=False)
    plt.show()
    return ani

if __name__ == "__main__":
    input_heights = [1,8,6,2,5,4,8,3,7]
    sol = Solution()
    result = sol.maxArea(input_heights, debug=True)  # expect 49

    # Find the pair that gives the max area for visualization and collect steps
    left, right = 0, len(input_heights) - 1
    max_area = 0
    best_left, best_right = left, right
    steps = []
    while left < right:
        area = (right - left) * min(input_heights[left], input_heights[right])
        steps.append((left, right, area))
        if area > max_area:
            max_area = area
            best_left, best_right = left, right
        if input_heights[left] < input_heights[right]:
            left += 1
        else:
            right -= 1
    # Animation: show every 2nd calculation, 1 second per frame
    ani = animate_container_steps(input_heights, steps, interval_ms=1000, every_nth=2)
    # To save animation as gif/mp4, uncomment:
    # ani.save('container_animation.gif', writer='pillow')

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

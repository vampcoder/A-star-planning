# A-star-planning

<b> Prerequisites</b>
- Python
- OpenCV
- Numpy
- Matplotlib

This is extended implementation of A-star algorithm.

For basic knowledge of A-star , one can refer following links : https://en.wikipedia.org/wiki/A*_search_algorithm

Now,  we are trying to guide a robot which has dimensions, so such robot should avoid obstacles. It would be better if that robot searches a path which is minimum at delta distance from obstacles.

Input Images

![Alt text](1.jpg?raw=true "Sample Image1")

![Alt text](2.jpg?raw=true "Sample Image2")


A* without applying clearance:

![Alt text](withoutClearance/1.jpg?raw=true "Sample Image1")

![Alt text](withoutClearance/2.jpg?raw=true "Sample Image2")

![Alt text](withoutClearance/3.jpg?raw=true "Sample Image3")


For this we preprocess our input images to create clearances for robot.

![Alt text](Clearance/1.jpg?raw=true "Sample Image4")

![Alt text](Clearance/2.jpg?raw=true "Sample Image5")

![Alt text](Clearance/3.jpg?raw=true "Sample Image6")

Now on the basis of these clearnace values, we deviced our cost function as normal distribution of this clearance value.

After applying A* on these images , we get following output:

Output Images:

![Alt text](output/1.jpg?raw=true "Sample Image7")

![Alt text](output/2.jpg?raw=true "Sample Image8")

![Alt text](output/3.jpg?raw=true "Sample Image9")

As you can see there is change in path followed by A-star. It avoids the obstacle to give shortest-optimal path.

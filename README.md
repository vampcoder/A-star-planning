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

![alt text][logo]
[logo]: 1.jpg "Sample Image1"

![alt text][logo]
[logo]: 2.jpg "Sample Image2"

![alt text][logo]
[logo]: 3.jpg "Sample Image3"

For this we preprocess our input images to create clearances for robot.

![alt text][logo]
[logo]: Clearance/1.jpg "Sample Image4"

![alt text][logo]
[logo]: Clearance/2.jpg "Sample Image5"

![alt text][logo]
[logo]: Clearance/3.jpg "Sample Image6"

Now on the basis of these clearnace values, we deviced our cost function as normal distribution of this clearance value.

After applying A* on these images , we get following output:

Output Images:

![alt text][logo]
[logo]: output/1.jpg "Sample Image7"

![alt text][logo]
[logo]: output/2.jpg "Sample Image8"

![alt text][logo]
[logo]: output/3.jpg "Sample Image9"

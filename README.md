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

![alt text][logo1]
[logo1]: 1.jpg "Sample Image1"

![alt text][logo2]
[logo2]: 2.jpg "Sample Image2"

![alt text][logo3]
[logo3]: 3.jpg "Sample Image3"

A* without applying clearance:

![alt text][logo10]
[logo10]: withoutClearance/1.jpg "Sample Image1"

![alt text][logo11]
[logo11]: withoutClearance/2.jpg "Sample Image2"

![alt text][logo12]
[logo12]: withoutClearance/3.jpg "Sample Image3"


For this we preprocess our input images to create clearances for robot.

![alt text][logo4]
[logo4]: Clearance/1.jpg "Sample Image4"

![alt text][logo5]
[logo5]: Clearance/2.jpg "Sample Image5"

![alt text][logo6]
[logo6]: Clearance/3.jpg "Sample Image6"

Now on the basis of these clearnace values, we deviced our cost function as normal distribution of this clearance value.

After applying A* on these images , we get following output:

Output Images:

![alt text][logo7]
[logo7]: output/1.jpg "Sample Image7"

![alt text][logo8]
[logo8]: output/2.jpg "Sample Image8"

![alt text][logo9]
[logo9]: output/3.jpg "Sample Image9"

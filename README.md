<a name="readme-top"></a>

<!-- Explanations -->
<!--
- This is a ReadMe template, cloned from https://github.com/othneildrew/Best-README-Template/
- Do a search and replace with your text editor for the following: `TAU-Graphics-Ex1-SeamCarving`,`Seam Carving Exercise`, `Content-aware image resizing using Seam Carving, created as part of the TAU Graphics course`
- fill any TODO sections:
  - Add a logo in images/logo.png
  - fill the table of contents
  - fill the About section - with Product screenshot and tech used

-->

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Boazius/TAU-Graphics-Ex1-SeamCarving">
    <img src="images/tauLogo.jpg" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Seam Carving Exercise</h3>

  <p align="center">
    Content-aware image resizing using Seam Carving, created as part of the TAU Graphics course 
    <br />
    <a href="https://github.com/Boazius/TAU-Graphics-Ex1-SeamCarving/issues">Report Bug</a>
    ·
    <a href="https://github.com/Boazius/TAU-Graphics-Ex1-SeamCarving/issues">Request Feature</a>
  </p>
</div>


<!-- ABOUT THE PROJECT -->
## About The Project
Exercise 1,  As part of the ["Fundamentals of Computer Graphics, Vision and Image Processing"](https://www.ims.tau.ac.il/Tal/Syllabus/Syllabus_L.aspx?course=0368323601&year=2022) course in Tel aviv university (2022). <br>
Made by [Boaz Yakubov](https://github.com/Boazius/) and [Noga Kinor](https://github.com/nogakinor)

Content-aware image resizing changes the image resolution while maintaining the aspect ratio of important regions - This is different from simple stretching or shrinking of the image, since it intelligently avoids impacting "important" areas of the image, and instead modifies the least important areas of the image (typically the background)

For example, for an image like this (1920x1080): 

<img src="images\camel.jpg" alt="alt_text" style="width:50%" />

if we wanted to resize it to 1500x1100 , we must find the "unimportant" areas - horizontal marked in black and vertical marked in red:

<img src="images\cameltime_vertical_seams.png" alt="alt_text" style="width:50%" />

<img src="images\cameltime_horizontal_seams.png" alt="alt_text" style="width:50%" />

and then delete these unimportant areas in the image to get the final resized image

<img src="images\cameltime_resized.png" alt="alt_text" style="width:50%" />

Note that the camels were not resized at all! only the background sky and desert was shrunk.

#### _in order to enlarge the image using this technique, we would simply duplicate these lines instead_

### This program performs image resizing using this technique on a specified image, and outputs:
- the resized image
- the original image with horizontal black lines (that will be deleted or duplicated)
- the _the partially resized_ image with vertical red lines (that will be deleted or duplicated)

#### The program optionally uses a "forward looking energy function" instead of the regular energy function, in order to reduce artifacts in the resized image

### Built With 
[![Python][Python-shield]][Python-url]
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Mathematical Background

In order to implement the Seam carving algorithm, we need to define an energy function that specifies the "importance" of each image pixel. we can calculate the pixel importance using the image gradient.

We computed it using the formula 
$E(i,j) =  \sqrt{\frac{{(\Delta_x)^2 + (\Delta_y)^2}}{2}} $
where $\Delta_x^2$ is the squared difference between the current and next horizontal pixel (in grayscale) and $\Delta_y^2$ is the same for vertical pixels

to find the optimal "Seams" to remove or duplicate , i.e the lines along the image:

- calculate the cost matrix M
- do k times:
    - find a path with the lowest total energy from one end of the image to the other.
    - delete or duplicate it

to resize the image both horizontally and vertically, we first change the width using the algorith and then the height on the partially resized image.

### Forward Looking energy function
Seam carving can introduce artifacts to the resized images. to reduce these artifacts, we implement a forward-looking energy function:

$M(i,j) = E(i,j) + \min\begin{cases}
M(i-1,j-1)+C_L(i,j), \\
M(i-1,j)+C_V(i,j) \\
M(i-1,j+1) + C_R(i,j)
\end{cases} $

where ($I_gs$ is the grayscale image) 

$C_L = |I_gs(i,j+1)-I_gs(i,j-1)|+|I_gs(i-1,j)-I_gs(i,j-1)|$

$C_V = |I_gs(i,j+1)-I_gs(i,j-1)|$

$C_R = |I_gs(i,j+1)-I_gs(i,j-1)|+|I_gs(i-1,j)-I_gs(i,j+1)|$

_when using the program, you can choose to use the previous energy function, or this forward looking energy function_

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started
To get a local copy up and running follow these simple steps.
- clone or download the repository
- open shell in the repository folder
- verify python and pip are installed ( use ``` python --version ``` and ```pip --version```)
- install requirements using  ``` pip install -r requirements.txt ```
- copy your desired images(s) into the folder, preferably into the imagesInput folder

now, to run the application simply type:
``` bash
python main.py
```

with the following arguments
- image_path (str) - an absolute / relative path to the image you want to process
- output_dir (str)– The output directory where you will save your outputs.
- height (int) – the output image height
- width (int) – the output image width
- resize_method (str) – a string representing the resize method. Could be one of the following: [‘nearest_neighbor’,‘seam_carving’]
- use_forward_implementation – a boolean flag indicates if forward looking energy function is used or not.
- output_prefix (str) – an optional string which will be used as a prefix to the output files. If set, the output files names will start with the given prefix. For seam carving, we will output two images, the resized image, and visualization of the chosen seems. So if --output_prefix is set to “my_prefix” then the output will be my_prefix_resized.png and my_prefix_horizontal _seams.png, my_prefix_vertical_seams.png. If the prefix is not set, then we will chose “img” as a default prefix.

so for example
``` bash
python main.py --image_path "imagesInput/tower.png" --output_dir "imagesOutput/" --height 900 --width 900 --resize_method "seam_carving" --output_prefix "my_prefix" --use_forward_implementation
```
will run the seam carving algorithm on tower.png and output the files:
- my_prefix_resized.png
- my_prefix_vertical_seams.png
- my_prefix_horizontal_seams.png

### Prerequisites
- Python
- pip

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License
Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

### I can be reached at at my email: boazyakubov@gmail.com

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* Noga Kinor for wonderful teamwork in this course
* Professor [Daniel Cohen-Or](https://www.tau.ac.il/profile/dcor) for teaching this course at TAU
* Roey Eliyahu Bar-On for instructing us on the subject at TAU

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- You can get more shields at img.shields.io , usage: [![Python][Python-shield]][Python-url] -->
[contributors-shield]: https://img.shields.io/github/contributors/Boazius/TAU-Graphics-Ex1-SeamCarving.svg?style=for-the-badge
[contributors-url]: https://github.com/Boazius/TAU-Graphics-Ex1-SeamCarving/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Boazius/TAU-Graphics-Ex1-SeamCarving.svg?style=for-the-badge
[forks-url]: https://github.com/Boazius/TAU-Graphics-Ex1-SeamCarving/network/members
[stars-shield]: https://img.shields.io/github/stars/Boazius/TAU-Graphics-Ex1-SeamCarving.svg?style=for-the-badge
[stars-url]: https://github.com/Boazius/TAU-Graphics-Ex1-SeamCarving/stargazers
[issues-shield]: https://img.shields.io/github/issues/Boazius/TAU-Graphics-Ex1-SeamCarving.svg?style=for-the-badge
[issues-url]: https://github.com/Boazius/TAU-Graphics-Ex1-SeamCarving/issues
[license-shield]: https://img.shields.io/github/license/Boazius/TAU-Graphics-Ex1-SeamCarving.svg?style=for-the-badge
[license-url]: https://github.com/Boazius/TAU-Graphics-Ex1-SeamCarving/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/boazyakubov
[product-screenshot]: images/screenshot.png
[Python-shield]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
[C-shield]: (https://img.shields.io/static/v1?style=for-the-badge&message=C&color=222222&logo=C&logoColor=A8B9CC&label=)
[CSharp-shield]: (https://img.shields.io/static/v1?style=for-the-badge&message=C+Sharp&color=512BD4&logo=C+Sharp&logoColor=FFFFFF&label=)
[CSharp-url]: (https://dotnet.microsoft.com/en-us/languages/csharp)
[Cplusplus-shield]: (https://img.shields.io/static/v1?style=for-the-badge&message=C%2B%2B&color=00599C&logo=C%2B%2B&logoColor=FFFFFF&label=)
[Cplusplus-url]: (https://cplusplus.com/)

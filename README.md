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

<img src="imagesInput\camel.jpg" alt="alt_text" style="width:50%" />

if we wanted to resize it to 1500x1100 , we must find the "unimportant" areas - horizontal marked in black and vertical marked in red:

<img src="imagesOutput\cameltime_horizontal_seams.png" alt="alt_text" style="width:50%" />
<img src="imagesOutput\cameltime_vertical_seams.png" alt="alt_text" style="width:50%" />

and then delete these unimportant areas in the image to get the final resized image

<img src="imagesOutput\cameltime_resized.png" alt="alt_text" style="width:50%" />

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

when using the program, you can choose to use the previous energy function, or this forward looking energy function.

<!-- GETTING STARTED -->
## Getting Started
<!-- TODO -->
This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites
<!-- TODO -->
This is an example of how to list things you need to use the software and how to install them.
* npm
  ```sh
  npm install npm@latest -g
  ```

### Installation
<!-- TODO -->
1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/Boazius/TAU-Graphics-Ex1-SeamCarving.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage
<!-- TODO -->
Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap
<!-- TODO -->
- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

See the [open issues](https://github.com/Boazius/TAU-Graphics-Ex1-SeamCarving/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing
<!-- TODO -->
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License
<!-- TODO -->
Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

### I can be reached at at my email: boazyakubov@gmail.com

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []()
* []()
* []()

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
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
[Python-shield]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
[C-shield]: (https://img.shields.io/static/v1?style=for-the-badge&message=C&color=222222&logo=C&logoColor=A8B9CC&label=)
[CSharp-shield]: (https://img.shields.io/static/v1?style=for-the-badge&message=C+Sharp&color=512BD4&logo=C+Sharp&logoColor=FFFFFF&label=)
[CSharp-url]: (https://dotnet.microsoft.com/en-us/languages/csharp)
[Cplusplus-shield]: (https://img.shields.io/static/v1?style=for-the-badge&message=C%2B%2B&color=00599C&logo=C%2B%2B&logoColor=FFFFFF&label=)
[Cplusplus-url]: (https://cplusplus.com/)
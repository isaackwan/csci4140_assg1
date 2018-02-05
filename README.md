# Web Instagram

Assignment 1, CSCI4140

## Live Demo URL

[https://vanilla-csci4140-rocks.a3c1.starter-us-west-1.openshiftapps.com](https://vanilla-csci4140-rocks.a3c1.starter-us-west-1.openshiftapps.com)

## OpenShift Instructions

Although the default Python S2I image is used, a [special image](https://github.com/isaackwan/python27-s2i-with-imagemagick) is used instead because ImageMagick is not available.

When configuring OpenShift, one should select "Build From Docker Image" and enter image "isaackwan/python27-s2i-with-imagemagick" under the "Image Configuration" section.

Furthermore, the environmental variable `CSCI4140_URL` is set to the URL of the instance.
You first need to build the image by running this in the Terminal:

docker build -t instapy .
Run in a Container

After the build succeeded, you can simply run the container with:

docker run --name=instapy -e INSTA_USER=<createurdeimagination> -e INSTA_PW=<Icarus14!?> -d instapy

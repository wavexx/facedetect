facedetect: a simple face detector for batch processing
-------------------------------------------------------

`facedetect` is a simple face detector for batch processing. It answers the
basic question: "Is there a face in this image?" and gives back either an exit
code or the coordinates of each detected face in the standard output.

The aim is to provide a basic command-line interface that's consistent and easy
to use with software such as ImageMagick_, while progressively improving the
detection algorithm over time.

`facedetect` is currently used in fgallery_ to improve the thumbnail cutting
region, so that faces are always centered.


Usage
-----

By default `facedetect` outputs the rectangles of all the detected faces::

  ./facedetect path/to/image.jpg
  289 139 56 56
  295 283 55 55

The output values are the X Y coordinates (from the lower-left corner),
followed by width and height. For debugging, you can examine the face positions
directly overlaid on the source image using the ``-o`` flag::

  ./facedetect -o test.jpg path/to/image.jpg

To simply check if an image contains a face, use the ``-q`` switch and check
the exit status::

  ./facedetect -q path/to/image.jpg
  echo $?

An exit status of 0 indicates the presence of at least one face. An exit status
of 2 means that no face could be detected (1 is reserved for failures).

The ``--center`` flag also exists for scripting convenience, and simply outputs
the X Y coordinates of face centers::

  ./facedetect --center path/to/image.jpg
  317 167
  322 310

The ``--biggest`` flag only outputs the biggest face in the image, while
``--best`` will attempt to select the face in focus and/or in the center of the
frame.


Examples
--------

Sorting images with and without faces
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The following example sorts pictures into two different "landscape"
and "portrait" directories using the exit code::

  for file in path/to/pictures/*.jpg; do
    name=$(basename "$file")
    if facedetect -q "$file"; then
      mv "$file" "path/to/portrait/$name"
    else
      mv "$file" "path/to/landscape/$name"
    fi
  done

Blurring faces within an image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The following example uses the coordinates from `facedetect` to pixelate the
faces in all the source images using `mogrify` (from ImageMagick_)::

  for file in path/to/pictures/*.jpg; do
    name=$(basename "$file")
    out="path/to/blurred/$name"
    cp "$file" "$out"
    facedetect "$file" | while read x y w h; do
      mogrify -gravity SouthWest -region "${w}x${h}+$x+y" \
	-scale '10%' -scale '1000%' "$out"
    done
  done


Dependencies
------------

The following software is currently required for `facedetect`:

- Python
- Python OpenCV
- OpenCV data files

On Debian/Ubuntu, you can install all the required dependencies with::

  sudo python python-opencv opencv-data

and then install `facedetect` with::

  sudo cp facedetect /usr/local/bin


Development status and ideas
----------------------------

Currently `facedetect` is a not much beyond a simple wrapper over the Haar
Cascade classifier of OpenCV and the ``frontalface_alt2`` profile, which
provided the best results in terms of accuracy/detection rate for the general,
real life photos at my disposal.

In terms of speed, the LBP classifier was faster. But while the general theory
states that it should also be more accurate, the ``lbp_frontalface`` profile
didn't provide comparable results, suggesting that additional training is
necessary. If some training dataset is found though, creating an LBP profile
would probably be a better solution especially for the processing speed.

``haar_profileface`` had too many false positives in my tests to be usable.
Using it in combination with ``haar_eye`` (and other face parts) though, to
reduce the false positive rates and/or rank the regions, might be a very good
solution instead.

Both LBP and Haar don't play too well with rotated faces. This is particularly
evident with "artistic" portraits shot at an angle. Pre-rotating the image
using the information from a Hough transform might boost the detection rate in
many cases, and should be relatively straightforward to implement.

There is currently not much difference between ``--biggest`` and ``--best``.
The latter simply forces a stricter minimum-neighbors in the cascade
classifier, reducing false positives. ``--best`` however should rank the
regions using a different criteria, such as a Contrast Transfer function
weighted by the region size and position. This would have the effect of
correctly choosing the focused face on a photo with considerable DOF, and or
picking up the central subject.


Authors and Copyright
---------------------

`facedetect` can be found at http://www.thregr.org/~wavexx/hacks/facedetect/

`facedetect` is distributed under GPL2 (see COPYING) WITHOUT ANY WARRANTY.
Copyright(c) 2011-2013 by wave++ "Yuri D'Elia" <wavexx@thregr.org>
facedetect's GIT repository is publicly accessible at::

  git://src.thregr.org/facedetect


.. _ImageMagick: http://www.imagemagick.org
.. _fgallery: http://www.thregr.org/~wavexx/software/fgallery/

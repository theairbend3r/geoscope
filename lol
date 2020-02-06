FROM python:3.6
MAINTAINER Akshaj Verma <akshajverma7@gmail.com>

RUN apt-get update \
    build-essential \
    cmake \
    git \
    libgtk2.0-dev \
    pkg-config \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libtbb2 \
    libtbb-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libjasper-dev \
    libdc1394-22-dev \
    libatlas-base-dev \
    gfortran pylint \
    gcc \
    g++ \
    libtiff5-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    pkg-config \
    libgtk2.0-dev \
    libopenblas-dev \
    libatlas-base-dev \
    liblapack-dev \
    libeigen3-dev \
    libtheora-dev \
    libvorbis-dev \
    libxvidcore-dev \
    libx264-dev \
    sphinx-common \
    libtbb-dev \
    yasm \
    libopencore-amrnb-dev \
    libopencore-amrwb-dev \
    libopenexr-dev \
    libgstreamer-plugins-base1.0-dev \
    libavcodec-dev \
    libavutil-dev \
    libavfilter-dev \
    libavformat-dev \
    libavresample-dev \
    ffmpeg

RUN pip install numpy

RUN wget opencv.zip https://github.com/opencv/opencv/archive/3.4.1.zip
RUN wget opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/3.4.1.zip
RUN unzip opencv.zip
RUN unzip opencv_contrib.zip
RUN cd ~/opencv-3.4.1/
RUN mkdir build
RUN cd build

RUN cmake -DOPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.4.1/modules/ \
-DBUILD_TIFF=ON \
-DBUILD_opencv_java=OFF \
-DWITH_CUDA=OFF \
-DWITH_OPENGL=ON \
-DWITH_OPENCL=ON \
-DWITH_IPP=ON \
-DWITH_TBB=ON \
-DWITH_EIGEN=ON \
-DWITH_V4L=ON \
-DBUILD_TESTS=OFF \
-DBUILD_PERF_TESTS=OFF \
-DCMAKE_BUILD_TYPE=RELEASE \
-DCMAKE_INSTALL_PREFIX=$(python -c "import sys; print(sys.prefix)") \
-DPYTHON_EXECUTABLE=$(which python) \
-DPYTHON_INCLUDE_DIR=$(python -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") \
-DPYTHON_PACKAGES_PATH=$(python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") ..

RUN make install

RUN mkdir /home/geoscope
WORKDIR /home/geoscope
ADD . /home/geoscope/
RUN pip install cmake
RUN pip install -r requirements.txt
RUN pip install gunicorn

EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]

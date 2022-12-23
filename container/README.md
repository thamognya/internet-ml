# Container / Docker for internet-ml

## Installation

To create Container / Docker you need to run:

```bash
make container-build
```

which is equivalent to:

```bash
make container-build VERSION=latest
```

You may provide name and version for the image.
Default name is `IMAGE := internet_ml`.
Default version is `VERSION := latest`.

```bash
make container-build IMAGE=some_name VERSION=0.1.0
```

## Usage

```bash
docker run -it --rm \
   -v $(pwd):/workspace \
   internet_ml bash
```

## How to clean up

To uninstall docker image run `make container-remove` with `VERSION`:

```bash
make container-remove VERSION=0.1.0
```

you may also choose the image name

```bash
make container-remove IMAGE=some_name VERSION=latest
```

If you want to clean all, including `build` and `pycache` run `make cleanup`

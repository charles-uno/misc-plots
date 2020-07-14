IMAGE := airplane-image
MOUNT := /workspace

.PHONY: all clean helper image in-image

all: helper

helper: image $(SOURCE)
	docker run --rm -v $(PWD):$(MOUNT) -w $(MOUNT) $(IMAGE) make in-image

image: Dockerfile
	docker build . -f Dockerfile -t $(IMAGE)

refresh: Dockerfile
	docker build . -f Dockerfile -t $(IMAGE) --no-cache

in-image:
	./scratch.py

clean:
	:

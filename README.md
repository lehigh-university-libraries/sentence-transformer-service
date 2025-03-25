# sentence-transformer-service

Simple web service to generate embeddings via an AI sentence transformer

## Developing locally

You can build the service via

```
docker build -t ghcr.io/lehigh-university-libraries/sentence-transformer:main .
```

Then make it available on your local machine with

```
docker run -p 8080:8080 ghcr.io/lehigh-university-libraries/sentence-transformer:main
```

Then open [http://localhost:8080/?q=foo+bar+baz](http://localhost:8080/?q=foo+bar+baz) in your web browser to see the embeddings for the sentence `foo bar baz`

## Updating model

The model is cached when the docker image is built with the script [cache.py](./cache.py)

So if we ever want to update the model this service uses, or update the model, we can modify that script accordingly.

## Attribution

Initial implementation inspired by https://github.com/jcoyne/code4lib-2024-ai-workshop

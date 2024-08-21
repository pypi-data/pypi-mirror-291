# bonn-py

NLP Category-Matching tools

A Rust microservice to match queries on the ONS Website to groupings in the ONS taxonomy

### Getting started

#### Set up taxonomy.json

This should be adapted from the taxonomy.json.example and placed in the root directory.

#### Download or create embeddings

These are most simply sourced as [pretrained fifu models](https://finalfusion.github.io/pretrained), but can be dynamically generated
using the embedded FinalFusion libraries.

To build wheels for distribution, use:

```
make
```

### Configuration

### Configuration

| Environment variable                     | Default                    | Description
| ----------------------------             | ---------                  | -----------
| CATEGORY_API_HOST                        | 0.0.0.0                    | Host
| CATEGORY_API_PORT                        | 28800                      | Port that the API is listening on
| CATEGORY_API_DUMMY_RUN                   | false                      | Returns empty list for testing purposes
| CATEGORY_API_DEBUG_LEVEL_FOR_DYNACONF    | "DEBUG"                    | Verbosity of dynaconf internal logging
| CATEGORY_API_ENVVAR_PREFIX_FOR_DYNACONF  | "CATEGORY_API"          | The prefix of which variables to be taken into dynaconf configuration
| CATEGORY_API_FIFU_FILE                   | "test_data/wiki.en.fifu"   | The location of the final fusion file
| CATEGORY_API_THRESHOLD                   | 0.4                        | Threshold of what's considered a low-scoring category
| CATEGORY_API_CACHE_S3_BUCKET             |                            | S3 for bucket for cache files in format "s3://"
| --------core variables------------       | ---------                  | -----------
| BONN_CACHE_TARGET                        | "cache.json"               | Cache target
| BONN_ELASTICSEARCH_HOST                  | "http://localhost:9200"    | Elasticsearch host
| BONN_REBUILD_CACHE                       | true                       | Should cache be rebuild
| BONN_TAXONOMY_LOCATION                   | "test_data/taxonomy.json"  | Location of taxonomy 
| BONN_ELASTICSEARCH_INDEX                 | "ons1639492069322"         | Location of taxonomy 
| BONN_WEIGHTING__C                        | 1                          | Word vectors based on the words in the category name
| BONN_WEIGHTING__SC                       | 2                          | Word vectors based on the words in the sub-categories name
| BONN_WEIGHTING__SSC                      | 2                          | Word vectors based on the words in the sub-sub-categories name
| BONN_WEIGHTING__WC                       | 6                          | Based on a bag of words found in the metadata of the datasets found in the categories
| BONN_WEIGHTING__WSSC                     | 8                          | Based on a bag of words found in the metadata of the datasets found in the sub-sub-categories


### Manual building

#### Quick Local Setup 

1. setup .env file - `$ cp .env.local .env` 

2. make wheels

2.  make sure you've placed taxonomy.json in the root folder (This should be obtained from ONS).

3. [TODO: genericize] you need an elasticsearch container forwarded to port:9200 (you can customize the port in .env) with a dump matching the appropriate schema `https://gitlab.com/flaxandteal/onyx/dp-search-api` in this readme you can checkout how to setup elasticsearch. 


#### Install finalfusion utils

``` bash
cd core
RUSTFLAGS="-C link-args=-lcblas -llapack" cargo install finalfusion-utils --features=opq
```

#### Optional: Convert the model to quantized fifu format

Note: if you try to use the full wiki bin you'll need about 128GB of RAM...

``` bash
finalfusion quantize -f fasttext -q opq <fasttext.bin> fasttext.fifu.opq
```

#### Install deps and build

``` bash
poetry shell
cd core
poetry install
cd ../api
poetry install
exit
```

#### Run

```bash
poetry run python -c "from bonn import FfModel; FfModel('test_data/wiki.en.fifu').eval('Hello')"
```

#### Create cache

You can create a cache with the following command:


```bash
poetry run python -m bonn.extract
```

This assumes that the correct environment variables for the NLP model, taxonomy and Elasticsearch are set.

### Algorithm

The following requirements were identified:

*   Fast response to live requests
*   Low running resource requirements, as far as possible
*   Ability to limit risk of unintended bias in results, and making results explainable
*   Minimal needed preprocessing of data (at least for first version)
*   Non-invasive - ensuring that the system can enhance existing work by ONS teams, with minimal changes required to incorporate
*   Runs effectively and reproducibly in ONS workflows

We found that the most effective approach was to use the standard Wikipedia unstructured word2vec model as the ML basis.

This has an additional advantage that we have been able to prototype incorporating other language category matching into the algorithm, although further work is required, including manual review by native speakers and initial results suggest that a larger language corpus would be required for training.

Using finalfusion libraries in Rust enables mmapping for memory efficiency.

#### Category Vectors

A bag of words is formed, to make a vector for the category - a weighted average of the terms, according to the attribute contributing it:

| Grouping                                       | Score basis                                                             |
| ---------------------------------------------- | ----------------------------------------------------------------------- |
| Category (top-level)                           | Literal words within title                                              |
| Subcategory (second-level)                     | Literal words within title                                              |
| Subsubcategory (third-level)                   | Literal words within title                                              |
| Related words across whole category            | Common thematic words across all datasets within the category           |
| Related words across subsubcategory            | Common thematic words across all datasets within the subsubcategory     |

To build a weighted bag of words, the system finds thematically-distinctive words occurring in dataset titles and descriptions
present in the categories, according to the taxonomy. The "thematic distinctiveness" of words in a dataset description
is defined by exceeding a similarity threshold to terms in the category title.

These can then be compared to search queries word-by-word, obtaining a score for each taxonomy entry, for a given phrase.

#### Scoring Adjustment

In addition to the direct cosine similarity of these vectors, we:

* remove any stopwords from the search scoring, with certain additional words that should not affect the category matching (“data”, “statistics”, “measure(s)”)
* apply an overall significance boost for a category, using the magnitude of the average word vector for its bag as a proxy for how “significant” it is that it matches a query phrase (so categories that match overly frequently, such as “population”, are slightly deprioritized)
* enhance or reduce contribution from each of the words in the query based on their commonality across categories.

To do the last, a global count of (lemmatized) words appearing in dataset descriptions/titles across all categories is made, and common terms are deprioritized within the bag according to an exponential decay function - this allows us to rely more heavily on words that strongly signpost a category (such as “education” or “school”) without being confounded by words many categories contain (such as “price” or “economic”).

Once per-category scores for a search phrase are obtained, we filter them based on:

* appearance thresholds, to ensure we only return matches over a minimal viable score;
* a signal-to-noise ratio filter (SNR) that returns a small number of notably high-scoring categories or a larger group of less distinguishable top scorers, according to a supplied SNR ratio.

### License

Prepared by Flax & Teal Limited for ONS Alpha project.
Copyright © 2022, Office for National Statistics (https://www.ons.gov.uk)

Released under MIT license, see [LICENSE](LICENSE.md) for details.

<h1 align="center">
  <img src="docs/icons/logo.png" alt="byteflow" width="200px">
  <br>
</h1>

# **Simple data workflows**

Byteflow is a microframework that makes it easier to retrieve information from APIs and regular websites.

Byteflow, unlike complex projects like Scrapy or simple libraries like BeautifulSoup, is extremely easy to use due to the unification of the information extraction process and at the same time has quite a wide range of functionality.

## **Why use Byteflow?**

* 🚀 Byteflow is built on top of asyncio and asynchronous libraries, which significantly speeds up your code in the context of I/O operations.

* 🔁 With Byteflow, there is no need to continuously customize the data scraping process. From project to project, you will have a single, transparent architecture.

* ![s3](https://raw.githubusercontent.com/DanchukIvan/byteflow/main/docs/img/amazons3.svg) ![kafka](https://raw.githubusercontent.com/DanchukIvan/byteflow/main/docs/img/apachekafka.svg) ![psql](https://raw.githubusercontent.com/DanchukIvan/byteflow/main/docs/img/postgresql.svg) ![clickhouse](https://raw.githubusercontent.com/DanchukIvan/byteflow/main/docs/img/clickhouse.svg) Byteflow allows you to route data to any backend: s3-like storage, database, network file system, broker/message bus, etc.

* ⚙️ Byteflow allows the user to choose what to do with the data: hold it in memory until a certain critical value accumulates, or immediately send it to the backend, perform pre-processing, or leave it as is.

## **Installation**

Installation is as simple as:

`
pip install Byteflow
`

## **Dependencies**

>The list of core Byteflow dependencies is represented by the following libraries:
>
> * aiohttp
> * aioitertools
> * fsspec
> * more-itertools
> * regex
> * uvloop (for Unix platforms)
> * yarl
> * dateparser

## **More information about the project**

You can learn more about Byteflow in the [project documentation](https://danchukivan.github.io/Byteflow/), including the API and Tutorial sections. Changes can be monitored in the Changelog section.

## **Project status**

Byteflow is currently a deep alpha project with an unstable API and limited functionality. Its use in production is **strictly not recommended**.

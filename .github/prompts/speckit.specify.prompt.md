---
agent: speckit.specify
---
### New Prompt

- add a new feature to publish the "Daily Readings" from the Catholic Lectionary
	- this "Daily Readings" feature will create a separate page for each day in a basic html format which is linked from the index page; these pages are also separate from the daily message
	- The readings are fetched from the USCCB.org readings site; there are existing python files found in this dir "https://github.com/etotten/catholic-liturgy-tools--try1/tree/001-liturgy-content-generator/src/scrapers" which can be used as the inspiration for this fetching, but the resulting .py files in this repo should have tests and be refactored if necessary.
	- the existing github action should be renamed to reflect that it will publish multiple things to the site; it will likely be used for even more features later, so we can keep the name generic
	- the index page has been changed; it should be generated such that the "/index.html" is not required on the end of the url for the page to render (e.g. https://etotten.github.io/catholic-liturgy-tools/ should render the index page)



### Prompt for spec 001-github-pages [DONE - kept for historical reference only]

- publish a hello world message using a github action to github site page (using Jekyll)
	- initially this message will just be the date in YYYY-MM-DD and "Hello Catholic World"
	- each day's message should be on it's own page which is linked from the index page
	- the published message should be in markdown format
	- provide a CLI to kickoff the runs, both via github actions (i.e. fully end-to-end) and directly via invoking the python scripts.
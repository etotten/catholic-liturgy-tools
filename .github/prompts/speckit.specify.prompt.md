---
agent: speckit.specify
---
### New Prompt

- We introduced an issue with the site restructure:
	- the index page for the site now only shows the latest reading and message; history of past generation and publishing is lost (at least to the index page, but I'm concerned it may be lost from the site completely)
	- this is probably due to no longer preserving the old generated content in the repo
	- the requirement which we need to re-establish is that we preserve everything we generated, so each time we publish to the site, there is more content added to what already exists
	- The index page should get longer as the links to the pages will grow; the latest publishing needs to be at the top for each feature.

### Initial Prompt for spec 003-site-content-restructure [DONE - kept for historical reference only]

Separate site content from the rest of the codebase and make more user-friendly:
  * all generated site content should go into a _site directory in order to help separate it from the code; under _site, we should use subdiretories to distinguish the generated files for different features (e.g. daily messages vs daily readings vs other future features)
	* make it so users can go to https://etotten.github.io/catholic-liturgy-tools for the index page and not have to go to https://etotten.github.io/catholic-liturgy-tools/_site/; this may require changes to the github pages settings or the repo structure
 * change the index page to be index.html and generate html instead of markdown; this will allow any user to click links regardless of whether they know how to read markdown or their client can render markdown


### Initial Prompt for spec 002-daily-readings [DONE - kept for historical reference only]

- add a new feature to publish the "Daily Readings" from the Catholic Lectionary
	- this "Daily Readings" feature will create a separate page for each day in a basic html format which is linked from the index page; these pages are also separate from the daily message
	- The readings are fetched from the USCCB.org readings site; there are existing python files found in this dir "https://github.com/etotten/catholic-liturgy-tools--try1/tree/001-liturgy-content-generator/src/scrapers" which can be used as the inspiration for this fetching, but the resulting .py files in this repo should have tests and be refactored if necessary.
	- the existing github action should be renamed to reflect that it will publish multiple things to the site; it will likely be used for even more features later, so we can keep the name generic
	- the index page has been changed; it should be generated such that the "/index.html" is not required on the end of the url for the page to render (e.g. https://etotten.github.io/catholic-liturgy-tools/ should render the index page)



### Initial Prompt for spec 001-github-pages [DONE - kept for historical reference only]

- publish a hello world message using a github action to github site page (using Jekyll)
	- initially this message will just be the date in YYYY-MM-DD and "Hello Catholic World"
	- each day's message should be on it's own page which is linked from the index page
	- the published message should be in markdown format
	- provide a CLI to kickoff the runs, both via github actions (i.e. fully end-to-end) and directly via invoking the python scripts.
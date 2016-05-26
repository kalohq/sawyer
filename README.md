# Sawyer -- the helpful changelog generator

*Always hopeful, yet discontent*  
*He knows changes aren't permanent*  
*But change is*

`sawyer` is your friend in changelog generation for Github projects, based on
pull requests closed since your last tagged version.

It supports Jinja2 templates, so you can make it your own.

## Quickstart

Install `sawyer`:

`python3 setup.py install`

Then, from a project's root directory:

`sawyer -u <username> <owner>/<repo> <previous-tag> <current-tag>`

This will output the changelog to the terminal. The current tag does not have
to exist, although the generated links will be broken if it doesn't eventually.
The previous tag is used to figure out what pull requests to include.

You will be prompted for a password unless you use the `-t` option to provide a
token.

Example:

`sawyer -u ctolsen -t <token> lystable/sawyer 0.1.0 0.2.0`

## Cleaning up your changelog

Since `sawyer` cannot (yet) organise your merged PRs into sections, you should
[do so yourself](https://github.com/olivierlacan/keep-a-changelog) for the time
being. 

It also assumes that you're creating a changelog for something that isn't yet
released – when you do, you should change `Unreleased` to an 
[ISO 8601](https://en.wikipedia.org/wiki/ISO_8601)-formatted date.

If the current limitations of the pull request organisation strategy -- or the
lack of it -- doesn't work out for you, simply pass sawyer the `--all-prs` flag
to print all PRs merged into the repository, ever. You'll have to clean the
backlog manually.

## Later plans

The intention is that `sawyer` will be able to manage a changelog completely.
Feeding in a well-formatted change log, it should be possible to generate
logs for a new release very quickly.

## License

Apache 2.0. See LICENSE for details

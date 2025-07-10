# Contributing to NetPulse

First off, thank you for considering contributing to NetPulse! It's people like you that make NetPulse such a great tool.

## Where do I go from here?

If you've noticed a bug or have a feature request, [make one](https://github.com/Code Savanna/netpulse/issues/new)! It's generally best if you get confirmation of your bug or approval for your feature request this way before starting to code.

### Fork & create a branch

If this is something you think you can fix, then [fork NetPulse](https://github.com/Code Savanna/netpulse/fork) and create a branch with a descriptive name.

A good branch name would be (where issue #325 is the ticket you're working on):

```sh
git checkout -b 325-add-japanese-translations
```

### Get the test suite running

Make sure you're on the latest version of `main` and that all tests pass.

```sh
# From the root of the project
npm test
```

### Implement your fix or feature

At this point, you're ready to make your changes! Feel free to ask for help; everyone is a beginner at first

### Make a Pull Request

At this point, you should switch back to your main branch and make sure it's up to date with NetPulse's main branch.

```sh
git remote add upstream git@github.com:dabwitso/netpulse.git
git checkout main
git pull upstream main
```

Then update your feature branch from your local copy of main, and push it!

```sh
git checkout 325-add-japanese-translations
git rebase main
git push --force-with-lease origin 325-add-japanese-translations
```

Finally, go to GitHub and [make a Pull Request](https://github.com/dabwitso/netpulse/compare)

### Keeping your Pull Request updated

If a maintainer asks you to "rebase" your PR, they're saying that a lot of code has changed, and that you need to update your branch so it's easier to merge.

To learn more about rebasing and merging, check out this guide on [merging vs. rebasing](https://www.atlassian.com/git/tutorials/merging-vs-rebasing).

## How to get in touch

You can chat with us on [Discord](https://discord.gg/your-server).

## Code of Conduct

Please be sure to read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

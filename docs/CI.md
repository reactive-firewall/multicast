# CI:

## Service providers
***

Continuous integration testing is handled by GitHub Actions and the generous CircleCI service.


## MATs
***

Minimal acceptance testing is run across multiple versions of python to ensure stable behavior
across a wide range of environments. Feature development and non-security related bug fixes are
done on development branches and then merged into the
[default branch (master)](https://github.com/reactive-firewall/multicast/blob/master/) for further
integration testing. This ensures the [stable](https://github.com/reactive-firewall/multicast/blob/stable/)
branch remains acceptable for production use.


## Testing
***

You can find all of the testing code in the aptly named `tests/` directory.
* Unit-testing is primarily done with the `unittest` framework.
* Functional testing is done via additional checks, including an end-to-end check invoking an
  actual pair of processes to test that `SAY` and `RECV` indeed work together.


## Dev Dependency Testing
***

### In a rush to get this module working? Then try using this with your own test:

```bash
#cd  /MY-AWESOME-DEV-PATH/multicast
make clean ; # cleans up from any previous tests hopefully
make test ; # runs the tests
make clean ; # cleans up for next test
```

#### Use PEP8 to check python code style? Great! Try this:

```bash
make clean ; # cleans up from any previous tests hopefully
make test-style ; # runs the tests
make clean ; # cleans up for next test
```

_draft_

---
#### Copyright (c) 2021-2024, Mr. Walls
[License - MIT](https://github.com/reactive-firewall/multicast/blob/stable/LICENSE.md)

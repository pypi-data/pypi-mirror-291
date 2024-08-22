https://github.com/DetachHead/basedpyright/issues/new

Document `all` option of `typeCheckingMode`

The new default of `typeCheckingMode` as `all` doesn't seem to be documented.

1. What is the difference between `all` and `strict`?
2. The original default was `standard`; but if `all` is even more comprehensive than `strict`, what was the reasoning behind making it the default? My concern is that this would make `basedpyright` overly pedantic, and that might not be a good default behavior; both due to false positives and for reducing the noise especially when working on existing codebases.

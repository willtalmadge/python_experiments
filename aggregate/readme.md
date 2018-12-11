This work was inspired by this talk by Rich Hicky
https://www.reddit.com/r/haskell/comments/a1ofh2/maybe_not_rich_hickey/

This is an attempt to take some of these ideas and implement them with python
language features. The closest off the shelf tool for accomplishing this is a
combination of mypy and PEP 544 protocols.

Of course this approach is not as rich as what Rich is suggestion. But, what
he is suggesting doesn't even exist in Clojure yet. This experiment explores
what can be done now with off the shelf tools.

The core idea is to avoid optional types in aggregates by simply leaving out
what you don't have. If you have extra stuff you should be able to ignore it.
We want to accomplish this while still being able to statically verify we are
using our functions correctly.

In this experiment I've tried doing the same thing in more typical patterns in
order compare and decide if the structural typing approach provides many
advantages.
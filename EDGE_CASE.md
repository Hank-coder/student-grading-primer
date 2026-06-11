# Edge Case: What happens to students without a mark in /stats?

## The Problem

The spec says `mark` is optional when creating a student via `POST /students`. So it's totally valid to create a student with just a name and course, and no mark. But when we hit `/stats`, the spec just says return count, average, min, max of "all student marks" — it doesn't say what to do with students who don't have a mark at all.

## What I decided

I chose to **skip** students with no mark when calculating stats. They just don't get counted.

## Why

A student with no mark hasn't been graded yet — it's not the same as getting 0. If I treated `None` as 0, the average would be wrong and the min would always be 0, which doesn't make sense. So I think it's more correct to only look at students who actually have a mark.

## How I did it

In the `/stats` route, I filter for students that have an integer mark before doing the calculations:

```python
marks = [s["mark"] for s in students if isinstance(s.get("mark"), int)]
```

If nobody has a mark (edge case of the edge case), I just return 0 for everything as a safe default.